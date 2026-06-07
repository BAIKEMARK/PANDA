from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.models.question import QuestionBank
from backend.app.core.common.exceptions import NotFoundException
from backend.app.modules.question.repositories.question_repository import QuestionRepository


class QuestionService:
    """题库领域服务（封装业务规则，具体持久化由 Repository 负责）"""

    def __init__(self, db: Session):
        self.db = db
        self.repo = QuestionRepository(db)

    def create(
        self,
        question_type: str,
        question_text: str,
        options: List[str],
        correct_answer: List[str],
        **kwargs,
    ) -> QuestionBank:
        return self.repo.create(
            question_type=question_type,
            question_text=question_text,
            options=options,
            correct_answer=correct_answer,
            **kwargs,
        )

    def get(self, question_id: str) -> Optional[QuestionBank]:
        return self.repo.get(question_id)

    def list(
        self,
        org_id: Optional[str] = None,
        question_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[QuestionBank]:
        return self.repo.list(
            org_id=org_id,
            question_type=question_type,
            status=status,
            skip=skip,
            limit=limit,
        )

    def update(self, question_id: str, **kwargs) -> QuestionBank:
        question = self.repo.update(question_id, **kwargs)
        if not question:
            raise NotFoundException(f"题目不存在: {question_id}")
        return question

    def delete(self, question_id: str) -> bool:
        deleted = self.repo.delete(question_id)
        if not deleted:
            raise NotFoundException(f"题目不存在: {question_id}")
        return True
