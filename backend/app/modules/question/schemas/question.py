from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class QuestionCreate(BaseModel):
    org_id: Optional[str] = Field(None, description="机构ID")
    scope: Optional[str] = Field("private", description="发布范围")
    question_type: str = Field(..., description="题型")
    question_text: str = Field(..., description="题干")
    options: List[str] = Field(..., description="选项")
    correct_answer: List[str] = Field(..., description="正确答案")
    explanation: Optional[str] = Field(None, description="解析")
    difficulty: Optional[str] = Field("medium", description="难度")
    knowledge_tags: Optional[List[str]] = Field(None, description="知识点标签")
    chapter_id: Optional[str] = Field(None, description="章节归属")
    status: Optional[str] = Field("draft", description="状态")


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[List[str]] = None
    explanation: Optional[str] = None
    difficulty: Optional[str] = None
    knowledge_tags: Optional[List[str]] = None
    chapter_id: Optional[str] = None
    status: Optional[str] = None


class QuestionResponse(BaseModel):
    id: str
    org_id: Optional[str]
    scope: str
    question_type: str
    question_text: str
    options: List[str]
    correct_answer: List[str]
    explanation: Optional[str]
    difficulty: str
    knowledge_tags: Optional[List[str]]
    chapter_id: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
