"""
全局异常处理中间件
统一处理所有异常，返回标准格式的错误响应
"""
import uuid
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from backend.app.core.common.exceptions import (
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    BadRequestException
)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    全局异常处理器
    
    Args:
        request: FastAPI请求对象
        exc: 异常对象
        
    Returns:
        JSONResponse: 标准格式的错误响应
    """
    # 生成请求ID（如果没有）
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    # 记录异常日志
    logger.opt(exception=exc).error(
        "请求异常 | request_id={} | path={} | method={} | error={}",
        request_id,
        request.url.path,
        request.method,
        exc
    )
    
    # 返回标准错误响应
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "服务器内部错误，请稍后重试",
            "request_id": request_id,
            "path": request.url.path
        }
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    """404 Not Found异常处理"""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    logger.warning(
        "资源未找到 | request_id={} | path={} | message={}",
        request_id,
        request.url.path,
        exc.detail
    )
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "not_found",
            "message": exc.detail,
            "request_id": request_id
        }
    )


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
    """401 Unauthorized异常处理"""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    logger.warning(
        "未授权访问 | request_id={} | path={} | message={}",
        request_id,
        request.url.path,
        exc.detail
    )
    
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "unauthorized",
            "message": exc.detail,
            "request_id": request_id
        }
    )


async def forbidden_exception_handler(request: Request, exc: ForbiddenException) -> JSONResponse:
    """403 Forbidden异常处理"""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    logger.warning(
        "权限不足 | request_id={} | path={} | message={}",
        request_id,
        request.url.path,
        exc.detail
    )
    
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "forbidden",
            "message": exc.detail,
            "request_id": request_id
        }
    )


async def bad_request_exception_handler(request: Request, exc: BadRequestException) -> JSONResponse:
    """400 Bad Request异常处理"""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    logger.warning(
        "请求参数错误 | request_id={} | path={} | message={}",
        request_id,
        request.url.path,
        exc.detail
    )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "bad_request",
            "message": exc.detail,
            "request_id": request_id
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """请求验证异常处理"""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    # 提取验证错误详情
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        "请求验证失败 | request_id={} | path={} | errors={}",
        request_id,
        request.url.path,
        errors
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "message": "请求参数验证失败",
            "details": errors,
            "request_id": request_id
        }
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """数据库异常处理"""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    logger.opt(exception=exc).error(
        "数据库错误 | request_id={} | path={} | error={}",
        request_id,
        request.url.path,
        exc
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "database_error",
            "message": "数据库操作失败，请稍后重试",
            "request_id": request_id
        }
    )
