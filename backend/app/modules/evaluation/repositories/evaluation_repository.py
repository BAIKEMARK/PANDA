"""
评估数据访问层（Repository）
评估报告CRUD操作
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from backend.app.models.evaluation import EvaluationReport


class EvaluationRepository:
    """评估数据访问仓库"""

    def __init__(self, db: Session):
        self.db = db

    def get_report_by_session(self, session_id: str) -> Optional[EvaluationReport]:
        """根据会话ID获取评估报告"""
        return self.db.query(EvaluationReport).filter(
            EvaluationReport.session_id == session_id
        ).first()

    def get_report_by_id(self, report_id: str) -> Optional[EvaluationReport]:
        """根据报告ID获取评估报告"""
        return self.db.query(EvaluationReport).filter(
            EvaluationReport.id == report_id
        ).first()

    def get_all_reports(self, skip: int = 0, limit: int = 100) -> List[EvaluationReport]:
        """获取所有评估报告"""
        return self.db.query(EvaluationReport).order_by(
            EvaluationReport.created_at.desc()
        ).offset(skip).limit(limit).all()

    def create_report(self, report_data: dict) -> EvaluationReport:
        """创建评估报告"""
        report = EvaluationReport(
            id=str(uuid.uuid4()),
            **report_data
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def delete_report(self, report_id: str) -> bool:
        """删除评估报告"""
        report = self.get_report_by_id(report_id)
        if report:
            self.db.delete(report)
            self.db.commit()
            return True
        return False
