"""
评估服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.models.evaluation import EvaluationReport
from backend.app.modules.evaluation.repositories.evaluation_repository import EvaluationRepository
from backend.app.schemas.evaluation import EvaluationReportResponse
from backend.app.common.exceptions import NotFoundException


class EvaluationService:
    """评估服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = EvaluationRepository(db)

    def get_report_by_session(self, session_id: str) -> Optional[EvaluationReport]:
        """根据会话ID获取评估报告"""
        return self.repository.get_report_by_session(session_id)

    def get_report_by_id(self, report_id: str) -> Optional[EvaluationReport]:
        """根据报告ID获取评估报告"""
        return self.repository.get_report_by_id(report_id)

    def get_all_reports(self, skip: int = 0, limit: int = 100) -> list:
        """获取所有评估报告"""
        reports = self.repository.get_all_reports(skip, limit)
        return [EvaluationReportResponse.from_orm_model(r) for r in reports]

    def delete_report(self, report_id: str) -> bool:
        """删除评估报告"""
        return self.repository.delete_report(report_id)

    def create_report(self, report_data: dict) -> EvaluationReport:
        """创建评估报告"""
        return self.repository.create_report(report_data)
