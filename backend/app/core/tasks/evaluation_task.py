"""
评估报告生成后台任务
使用线程池异步生成评估报告
"""
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from backend.app.db.database import SessionLocal
from backend.app.models.evaluation import EvaluationReport
from backend.app.modules.evaluation.agents.mentor_agent import MentorAgent
from backend.app.core.config.logging import get_logger

logger = get_logger(__name__)

# 创建线程池（最多4个并发任务）
executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="eval_task")


def _format_evaluation_error(error: Exception) -> str:
    """Return a concise user-facing message while full details stay in logs."""
    error_text = str(error)
    if "OutputParserException" in error_text or "Invalid json output" in error_text:
        return "评估模型输出格式异常，系统已记录详情，请重新生成评估报告。"
    if "会话不存在" in error_text:
        return error_text
    return error_text[:500]


def generate_evaluation_async(session_id: str, report_id: Optional[str] = None):
    """
    异步生成评估报告
    
    Args:
        session_id: 会话ID
        report_id: 报告ID（如果已创建）
    """
    # 提交到线程池执行
    future = executor.submit(_generate_evaluation_task, session_id, report_id)
    logger.info(f"评估任务已提交 | session_id={session_id} | report_id={report_id}")
    return future


def _generate_evaluation_task(session_id: str, report_id: Optional[str] = None):
    """
    评估报告生成任务（在后台线程中执行）

    Args:
        session_id: 会话ID
        report_id: 报告ID
    """
    db: Session = SessionLocal()

    try:
        logger.info(f"开始生成评估报告 | session_id={session_id}")

        # 1. 获取或创建报告记录
        if report_id:
            report = db.query(EvaluationReport).filter(
                EvaluationReport.id == report_id
            ).first()
        else:
            report = db.query(EvaluationReport).filter(
                EvaluationReport.session_id == session_id
            ).first()

        if not report:
            # 创建新报告记录
            report = EvaluationReport(
                id=str(uuid.uuid4()),
                session_id=session_id,
                status="generating"
            )
            db.add(report)
            db.commit()
            logger.info(f"创建报告记录 | report_id={report.id}")
        else:
            # 更新状态为生成中
            report.status = "generating"
            report.error_message = None
            db.commit()
            logger.info(f"更新报告状态为生成中 | report_id={report.id}")

        # 2. 调用MentorAgent生成评估
        mentor_agent = MentorAgent(db, subscribe_events=False)

        try:
            # 生成评估报告（这是耗时操作）
            generated_report = mentor_agent.generate_evaluation(session_id)

            # 3. 更新报告数据
            # 检查是否已有其他方式生成的报告（通过事件总线自动生成）
            if generated_report.id != report.id:
                # 已有其他方式生成的报告，删除当前重复的报告记录
                logger.info(f"发现重复报告，删除当前记录 | report_id={report.id} | existing_report_id={generated_report.id}")
                db.delete(report)
                db.commit()
                return generated_report

            # 使用当前报告记录，更新数据
            report.status = "completed"
            report.completed_at = datetime.now(timezone.utc)

            report.total_score = generated_report.total_score
            report.level_assessment = generated_report.level_assessment
            report.radar_a_risk_identification = generated_report.radar_a_risk_identification
            report.radar_b_communication = generated_report.radar_b_communication
            report.radar_c_skill_application = generated_report.radar_c_skill_application
            report.radar_d_safety_management = generated_report.radar_d_safety_management
            report.radar_e_self_efficacy = generated_report.radar_e_self_efficacy
            report.state_analysis = generated_report.state_analysis
            report.detailed_feedback = generated_report.detailed_feedback
            report.technical_guidance = generated_report.technical_guidance
            report.meta_data = generated_report.meta_data

            db.commit()

            logger.info(
                f"评估报告生成成功 | session_id={session_id} | "
                f"report_id={report.id} | score={report.total_score}"
            )

            return report

        except ValueError as e:
            # 处理会话不存在的错误
            if "会话不存在" in str(e):
                logger.warning(f"会话不存在，跳过评估 | session_id={session_id}")
                report.status = "failed"
                report.error_message = f"会话不存在: {session_id}"
                db.commit()
                return None
            else:
                # 其他 ValueError
                report.status = "failed"
                report.error_message = _format_evaluation_error(e)
                db.commit()
                logger.error(
                    f"评估报告生成失败 | session_id={session_id} | "
                    f"report_id={report.id} | error={str(e)}",
                    exc_info=True
                )
                raise

        except Exception as e:
            # 生成失败，更新状态
            report.status = "failed"
            report.error_message = _format_evaluation_error(e)
            db.commit()

            logger.error(
                f"评估报告生成失败 | session_id={session_id} | "
                f"report_id={report.id} | error={str(e)}",
                exc_info=True
            )
            raise

    except Exception as e:
        logger.error(f"评估任务执行失败 | session_id={session_id} | error={str(e)}", exc_info=True)
        db.rollback()
        raise

    finally:
        try:
            # 尝试清除该用户的 Dashboard 缓存
            from backend.app.models.chat import ChatSession
            session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if session and session.user_id:
                from backend.app.core.services.redis_cache import redis_cache
                from backend.app.core.config.settings import settings
                if settings.CACHE_ENABLED:
                    redis_cache.delete(f"dashboard:{session.user_id}")
        except Exception as cache_err:
            logger.error(f"Failed to clear cache: {cache_err}")
        db.close()


def get_report_status(session_id: str) -> Optional[dict]:
    """
    获取报告生成状态
    
    Args:
        session_id: 会话ID
        
    Returns:
        报告状态信息
    """
    db: Session = SessionLocal()
    
    try:
        report = db.query(EvaluationReport).filter(
            EvaluationReport.session_id == session_id
        ).first()
        
        if not report:
            return None
        
        return {
            "report_id": report.id,
            "session_id": report.session_id,
            "status": report.status,
            "error_message": report.error_message,
            "created_at": report.created_at.isoformat() if report.created_at else None,
            "completed_at": report.completed_at.isoformat() if report.completed_at else None,
            "total_score": report.total_score if report.status == "completed" else None
        }
    
    finally:
        db.close()
