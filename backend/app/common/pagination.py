"""
分页工具模块
提供统一的分页功能
"""
from typing import TypeVar, Generic, List
from pydantic import BaseModel
from sqlalchemy.orm import Query

T = TypeVar('T')


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = 1
    page_size: int = 10
    
    def get_offset(self) -> int:
        """计算偏移量"""
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """获取限制数量"""
        return self.page_size


class PaginatedResult(Generic[T]):
    """分页结果"""
    def __init__(
        self,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "items": self.items,
            "total": self.total,
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": self.total_pages
        }


def paginate_query(
    query: Query,
    page: int = 1,
    page_size: int = 10
) -> PaginatedResult:
    """
    对SQLAlchemy查询进行分页
    
    Args:
        query: SQLAlchemy查询对象
        page: 页码（从1开始）
        page_size: 每页数量
    
    Returns:
        PaginatedResult: 分页结果
    """
    # 确保参数有效
    page = max(1, page)
    page_size = max(1, min(page_size, 100))  # 限制最大100条
    
    # 计算总数
    total = query.count()
    
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 获取数据
    items = query.offset(offset).limit(page_size).all()
    
    return PaginatedResult(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


def paginate_list(
    items: List[T],
    page: int = 1,
    page_size: int = 10
) -> PaginatedResult[T]:
    """
    对列表进行分页
    
    Args:
        items: 数据列表
        page: 页码（从1开始）
        page_size: 每页数量
    
    Returns:
        PaginatedResult: 分页结果
    """
    # 确保参数有效
    page = max(1, page)
    page_size = max(1, min(page_size, 100))
    
    # 计算总数
    total = len(items)
    
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 获取分页数据
    paginated_items = items[offset:offset + page_size]
    
    return PaginatedResult(
        items=paginated_items,
        total=total,
        page=page,
        page_size=page_size
    )
