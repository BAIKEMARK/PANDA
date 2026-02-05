from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
import json

from backend.app.models.question import QuestionBank
from backend.app.common.exceptions import NotFoundException


class QuestionService:
    def __init__(self, db: Session):
        self.db = db

    def _maybe_json_load(self, value):
        if value is None:
            return None
        if isinstance(value, (list, dict)):
            return value
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def create(self, question_type: str, question_text: str, options: List[str],
               correct_answer: List[str], **kwargs) -> QuestionBank:
        question = QuestionBank(
            id=str(uuid4()),
            question_type=question_type,
            question_text=question_text,
            options=json.dumps(options),
            correct_answer=json.dumps(correct_answer),
            knowledge_tags=json.dumps(kwargs.get('knowledge_tags', [])) if kwargs.get('knowledge_tags') else None,
            **{k: v for k, v in kwargs.items() if k not in ['knowledge_tags']}
        )
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        question.options = self._maybe_json_load(question.options)
        question.correct_answer = self._maybe_json_load(question.correct_answer)
        question.knowledge_tags = self._maybe_json_load(question.knowledge_tags)
        return question

    def get(self, question_id: str) -> Optional[QuestionBank]:
        question = self.db.query(QuestionBank).filter(QuestionBank.id == question_id).first()
        if question:
            question.options = self._maybe_json_load(question.options)
            question.correct_answer = self._maybe_json_load(question.correct_answer)
            question.knowledge_tags = self._maybe_json_load(question.knowledge_tags)
        return question

    def list(self, org_id: Optional[str] = None, question_type: Optional[str] = None,
             status: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[QuestionBank]:
        query = self.db.query(QuestionBank)
        if org_id:
            query = query.filter(QuestionBank.org_id == org_id)
        if question_type:
            query = query.filter(QuestionBank.question_type == question_type)
        if status:
            query = query.filter(QuestionBank.status == status)
        questions = query.offset(skip).limit(limit).all()
        for question in questions:
            question.options = self._maybe_json_load(question.options)
            question.correct_answer = self._maybe_json_load(question.correct_answer)
            question.knowledge_tags = self._maybe_json_load(question.knowledge_tags)
        return questions

    def update(self, question_id: str, **kwargs) -> QuestionBank:
        question = self.get(question_id)
        if not question:
            raise NotFoundException(f"题目不存在: {question_id}")
        
        if 'options' in kwargs and kwargs['options']:
            kwargs['options'] = json.dumps(kwargs['options'])
        if 'correct_answer' in kwargs and kwargs['correct_answer']:
            kwargs['correct_answer'] = json.dumps(kwargs['correct_answer'])
        if 'knowledge_tags' in kwargs and kwargs['knowledge_tags']:
            kwargs['knowledge_tags'] = json.dumps(kwargs['knowledge_tags'])
        
        for key, value in kwargs.items():
            if hasattr(question, key) and value is not None:
                setattr(question, key, value)
        
        self.db.commit()
        self.db.refresh(question)
        question.options = self._maybe_json_load(question.options)
        question.correct_answer = self._maybe_json_load(question.correct_answer)
        question.knowledge_tags = self._maybe_json_load(question.knowledge_tags)
        return question

    def delete(self, question_id: str) -> bool:
        question = self.get(question_id)
        if not question:
            raise NotFoundException(f"题目不存在: {question_id}")
        
        self.db.delete(question)
        self.db.commit()
        return True
