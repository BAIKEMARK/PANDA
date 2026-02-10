"""
统一响应格式模块
确保前后端数据格式一致
"""
from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """统一响应模型"""
    success: bool = True
    message: str = "操作成功"
    data: Optional[T] = None
    code: int = 200


class PaginationMeta(BaseModel):
    """分页元数据"""
    page: int = 1
    page_size: int = 10
    total: int = 0
    total_pages: int = 0


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    success: bool = True
    message: str = "查询成功"
    data: list[T] = []
    meta: PaginationMeta
    code: int = 200


def success_response(
    data: Any = None,
    message: str = "操作成功",
    code: int = 200
) -> dict:
    """成功响应"""
    return {
        "success": True,
        "message": message,
        "data": data,
        "code": code
    }


def error_response(
    message: str = "操作失败",
    code: int = 400,
    data: Any = None
) -> dict:
    """错误响应"""
    return {
        "success": False,
        "message": message,
        "data": data,
        "code": code
    }


def paginated_response(
    data: list,
    page: int,
    page_size: int,
    total: int,
    message: str = "查询成功"
) -> dict:
    """分页响应"""
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        },
        "code": 200
    }
