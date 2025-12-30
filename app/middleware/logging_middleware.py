import time
from fastapi import Request
from loguru import logger
from app.constants.services import ALLOW_SERVICE

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

        path_parts = request.url.path.strip("/").split("/")
        service_entity = path_parts[2] if len(path_parts) > 2 else None

        service_logger = logger

        if service_entity:
            if service_entity in ALLOW_SERVICE:
                service_logger = logger.bind(service=service_entity)

        service_logger.info(
            "HTTP {method} {path} | Status: {status} | Time: {time}ms | IP: {ip}",
            method=request.method,
            path=request.url.path,
            status=status_code,
            time=process_time,
            ip=request.client.host if request.client else "unknown",
        )

        return response

    except Exception as exc:
        process_time = round((time.time() - start_time) * 1000, 2)

        logger.exception(
            "HTTP {method} {path} | FAILED | Time: {time}ms | IP: {ip}",
            method=request.method,
            path=request.url.path,
            time=process_time,
            ip=request.client.host if request.client else "unknown",
        )
        raise exc

