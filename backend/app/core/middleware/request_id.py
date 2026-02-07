"""
请求ID追踪中间件
为每个请求生成唯一ID，便于日志追踪和问题排查
"""
import uuid
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from loguru import logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    """请求ID中间件 - 为每个请求生成唯一标识"""
    
    async def dispatch(self, request: Request, call_next):
        """
        处理请求，添加请求ID
        
        Args:
            request: FastAPI请求对象
            call_next: 下一个中间件或路由处理器
            
        Returns:
            Response: 响应对象（包含X-Request-ID头）
        """
        # 生成请求ID（优先使用客户端提供的，否则生成新的）
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # 保存到request.state，供后续使用
        request.state.request_id = request_id
        
        # 记录请求开始时间
        start_time = time.time()
        
        # 记录请求日志
        logger.info(
            f"请求开始 | request_id={request_id} | "
            f"method={request.method} | path={request.url.path} | "
            f"client={request.client.host if request.client else 'unknown'}"
        )
        
        # 处理请求
        try:
            response: Response = await call_next(request)
            
            # 计算请求耗时
            duration = time.time() - start_time
            
            # 添加请求ID到响应头
            response.headers["X-Request-ID"] = request_id
            
            # 记录响应日志
            logger.info(
                f"请求完成 | request_id={request_id} | "
                f"status={response.status_code} | "
                f"duration={duration:.3f}s"
            )
            
            return response
            
        except Exception as e:
            # 计算请求耗时
            duration = time.time() - start_time
            
            # 记录异常日志
            logger.error(
                f"请求异常 | request_id={request_id} | "
                f"duration={duration:.3f}s | error={str(e)}",
                exc_info=True
            )
            
            # 重新抛出异常，让全局异常处理器处理
            raise
