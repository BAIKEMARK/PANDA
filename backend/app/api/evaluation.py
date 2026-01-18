"""
Evaluation API Router
评估API路由 - 管理评估报告
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.schemas.evaluation import EvaluationReportResponse
from backend.app.services.mentor_agent import MentorAgent
from backend.app.models.evaluation import EvaluationReport
from backend.app.common.exceptions import NotFoundException

router = APIRouter(prefix="/evaluation", tags=["评估"])


@router.post("/sessions/{session_id}/evaluate", response_model=EvaluationReportResponse, status_code=status.HTTP_201_CREATED)
async def evaluate_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    生成会话评估报告

    调用Mentor-Agent分析对话历史，基于THP五维评分标准生成评估报告。

    - **session_id**: 会话ID
    """
    try:
        # 检查是否已有评估报告
        existing_report = db.query(EvaluationReport).filter(
            EvaluationReport.session_id == session_id
        ).first()

        if existing_report:
            # 如果已有报告，直接返回
            return EvaluationReportResponse.from_orm_model(existing_report)

        # 调用Mentor-Agent生成评估
        mentor_agent = MentorAgent(db)
        report = mentor_agent.generate_evaluation(session_id)

        return EvaluationReportResponse.from_orm_model(report)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"评估生成失败: {str(e)}"
        )


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
    report = db.query(EvaluationReport).filter(
        EvaluationReport.session_id == session_id
    ).first()

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
    report = db.query(EvaluationReport).filter(
        EvaluationReport.id == report_id
    ).first()

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
    reports = db.query(EvaluationReport).order_by(
        EvaluationReport.created_at.desc()
    ).offset(skip).limit(limit).all()

    return [EvaluationReportResponse.from_orm_model(report) for report in reports]


@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """
    删除评估报告

    - **report_id**: 报告ID
    """
    report = db.query(EvaluationReport).filter(
        EvaluationReport.id == report_id
    ).first()

    if not report:
        raise NotFoundException("评估报告不存在")

    db.delete(report)
    db.commit()

    return None