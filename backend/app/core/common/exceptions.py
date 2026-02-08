"""
Common Exceptions
公共异常类
"""
from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """基础API异常"""
    def __init__(self, status_code: int, detail: str = None):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(BaseAPIException):
    """资源未找到异常"""
    def __init__(self, detail: str = "资源不存在"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(BaseAPIException):
    """错误请求异常"""
    def __init__(self, detail: str = "请求参数错误"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ConflictException(BaseAPIException):
    """冲突异常"""
    def __init__(self, detail: str = "资源冲突"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UnauthorizedException(BaseAPIException):
    """未授权异常"""
    def __init__(self, detail: str = "未授权访问"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(BaseAPIException):
    """禁止访问异常"""
    def __init__(self, detail: str = "权限不足"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)