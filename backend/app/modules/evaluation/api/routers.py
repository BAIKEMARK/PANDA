"""
评估 API 路由
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from backend.app.db.database import get_db
from backend.app.schemas.evaluation import EvaluationReportResponse
from backend.app.modules.evaluation.services.evaluation_service import EvaluationService
from backend.app.modules.evaluation.agents.mentor_agent import MentorAgent
from backend.app.core.common.exceptions import NotFoundException
from backend.app.core.tasks.evaluation_task import generate_evaluation_async, get_report_status
from backend.app.models.evaluation import EvaluationReport

router = APIRouter(prefix="/evaluation", tags=["评估"])


@router.post("/sessions/{session_id}/evaluate", status_code=status.HTTP_202_ACCEPTED)
async def evaluate_session_async(
    session_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    异步生成会话评估报告
    
    立即返回202 Accepted，报告在后台生成。
    客户端应该轮询 GET /evaluation/sessions/{session_id}/status 查询生成状态。

    - **session_id**: 会话ID
    
    Returns:
        {
            "message": "评估报告生成任务已提交",
            "session_id": "xxx",
            "report_id": "xxx",
            "status": "generating"
        }
    """
    try:
        service = EvaluationService(db)

        # 检查是否已有评估报告
        existing_report = service.get_report_by_session(session_id)
        if existing_report:
            if existing_report.status == "completed":
                return {
                    "message": "评估报告已存在",
                    "session_id": session_id,
                    "report_id": existing_report.id,
                    "status": "completed"
                }
            elif existing_report.status == "generating":
                return {
                    "message": "评估报告正在生成中",
                    "session_id": session_id,
                    "report_id": existing_report.id,
                    "status": "generating"
                }
            elif existing_report.status == "failed":
                # 重新生成
                existing_report.status = "generating"
                existing_report.error_message = None
                db.commit()
                generate_evaluation_async(session_id, existing_report.id)
                return {
                    "message": "评估报告重新生成中",
                    "session_id": session_id,
                    "report_id": existing_report.id,
                    "status": "generating"
                }
        
        # 创建新的报告记录
        report_id = str(uuid.uuid4())
        new_report = EvaluationReport(
            id=report_id,
            session_id=session_id,
            status="generating",
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_report)
        db.commit()
        
        # 提交后台任务
        generate_evaluation_async(session_id, report_id)
        
        return {
            "message": "评估报告生成任务已提交",
            "session_id": session_id,
            "report_id": report_id,
            "status": "generating"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"评估任务提交失败: {str(e)}"
        )


@router.get("/sessions/{session_id}/status")
async def get_evaluation_status(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    查询评估报告生成状态
    
    - **session_id**: 会话ID
    
    Returns:
        {
            "report_id": "xxx",
            "session_id": "xxx",
            "status": "pending|generating|completed|failed",
            "error_message": "错误信息（如果失败）",
            "created_at": "2026-02-07T...",
            "completed_at": "2026-02-07T...",
            "total_score": 85
        }
    """
    status_info = get_report_status(session_id)
    
    if not status_info:
        raise NotFoundException("评估报告不存在")
    
    return status_info


@router.get("/sessions/{session_id}/report", response_model=EvaluationReportResponse)
async def get_evaluation_report(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    获取会话评估报告

    返回指定会话的评估报告。如果报告不存在，返回404。

    - **session_id**: 会话ID
    """
    service = EvaluationService(db)
    report = service.get_report_by_session(session_id)

    if not report:
        raise NotFoundException("评估报告不存在")

    return EvaluationReportResponse.from_orm_model(report)


@router.get("/reports/{report_id}", response_model=EvaluationReportResponse)
async def get_report_by_id(
    report_id: str,
    db: Session = Depends(get_db)
):
    """
    根据报告ID获取评估报告

    - **report_id**: 报告ID
    """
    service = EvaluationService(db)
    report = service.get_report_by_id(report_id)

    if not report:
        raise NotFoundException("评估报告不存在")

    return EvaluationReportResponse.from_orm_model(report)


@router.get("/reports", response_model=List[EvaluationReportResponse])
async def list_all_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取所有评估报告列表

    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数
    """
    service = EvaluationService(db)
    return service.get_all_reports(skip, limit)


@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """
    删除评估报告

    - **report_id**: 报告ID
    """
    service = EvaluationService(db)
    success = service.delete_report(report_id)
    if not success:
        raise NotFoundException("评估报告不存在")
    return None
