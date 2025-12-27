import time
from fastapi import Request
from loguru import logger
from sqlmodel import Session
from app.database import engine


async def loguru_logging_middleware(request: Request, call_next):
    """
    Middleware for logging request timing and status using Loguru.
    
    Args:
        request (Request): HTTP Request.
        call_next (Callable): Next middleware/handler.
        
    Returns:
        Response: HTTP Response.
    """
    start_time = time.time()

    try:
        response = await call_next(request)
        status_code = response.status_code

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            "HTTP {method} {path} | Status: {status} | Time: {time}ms | IP: {ip}",
            method=request.method,
            path=request.url.path,
            status=status_code,
            time=process_time,
            ip=request.client.host if request.client else "unknown"
        )

        return response

    except Exception as exc:
        process_time = round((time.time() - start_time) * 1000, 2)

        logger.error(
            "HTTP {method} {path} | FAILED | Time: {time}ms | IP: {ip} | Error: {error}",
            method=request.method,
            path=request.url.path,
            time=process_time,
            ip=request.client.host if request.client else "unknown",
            error=str(exc)
        )

        raise exc

       
