from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlmodel import Session

from app.database import engine
from app.utils.activity_logger import create_log_activity
from app.core.logger import logger
from app.utils.enum_security import encrypt_secure_fields

import json


def get_action_from_method(method: str) -> str:
    """
    Map HTTP methods to CRUD actions.
    
    Args:
        method (str): HTTP method (GET, POST, etc.).
        
    Returns:
        str: Mapped action (CREATE, READ, UPDATE, DELETE).
    """
    method = method.upper()
    if method == "POST":
        return "CREATE"
    elif method in ("PUT", "PATCH"):
        return "UPDATE"
    elif method == "DELETE":
        return "DELETE"
    elif method == "GET":
        return "READ"
    return "UNKNOWN"


from app.constants.excluded_routes import EXCLUDED_PREFIXES

class ActivityLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all HTTP requests and responses for activity tracking.
    
    Captures:
    - Request Body (Encrypted if sensitive)
    - Response Body (Encrypted if sensitive)
    - Status Codes
    - User ID (from query params)
    """

    async def dispatch(self, request: Request, call_next):
        """
        Intercepts requests to log activity and handle transitions.
        """
        db: Session = Session(engine)
        request.state.db = db 
        
        # SKIP LOGGING for configured routes to prevent recursion or spam
        # Checks if any excluded prefix is present in the request URL path AND if the method matches
        for prefix, methods in EXCLUDED_PREFIXES.items():
            if prefix in request.url.path:
                if "*" in methods or request.method in methods:
                    return await call_next(request)

        status = "SUCCESS"
        body_bytes = await request.body()
        request_body = None

        if body_bytes:
            try:
                request_body = json.loads(body_bytes)
            except Exception:
                request_body = body_bytes.decode(errors="ignore")

        # print request log
        logger.info(
            f"REQUEST | {request.method} {request.url.path} | BODY = {request_body}"
        )

        # set user_id for audit
        user_id = request.query_params.get("user_id")
        if user_id:
            try:
                # Attach user_id to DB session info for AuditLog triggers
                # [MERGE INSTRUCTION]: When merging with Auth system, replace the line below with:
                # user_id = request.state.user.id  (or equivalent token-based retrieval)
                db.info["user_id"] = int(user_id)
            except ValueError:
                pass

        try:
            response = await call_next(request)

            response_body_bytes = b""
            async for chunk in response.body_iterator:
                response_body_bytes += chunk

            try:
                response_body = json.loads(response_body_bytes)
            except Exception:
                response_body = response_body_bytes.decode(errors="ignore")

            if response.status_code >= 400:
                status = "FAILED"

            response = Response(
                content=response_body_bytes,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        except Exception as exc:
            status = "FAILED"
            logger.error(
                f"ERROR | {request.method} {request.url.path} | {str(exc)}"
            )
            raise exc

        finally:
            try:
                # Extract entity name and ID from URL path
                # Expects structure like /api/v1/{entity}/{id}
                path_parts = request.url.path.strip("/").split("/")
                entity = path_parts[2] if len(path_parts) > 2 else None
                entity_id = None
                if len(path_parts) > 3 and path_parts[3].isdigit():
                    entity_id = int(path_parts[3])
                elif len(path_parts) > 1 and path_parts[1].isdigit():
                     # Fallback logic depending on route structure
                    entity_id = int(path_parts[1])

                metadata = {
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "request_body": encrypt_secure_fields(request_body),
                    "response_body": encrypt_secure_fields(response_body),
                    "query_params": dict(request.query_params),
                    "headers": dict(request.headers),
                }

                create_log_activity(
                    db=db,
                    request=request,
                    action=get_action_from_method(request.method),
                    entity=entity,
                    entity_id=entity_id,
                    status=status,
                    status_code=response.status_code,
                    extra_data=metadata,
                )

            except Exception as log_error:
                logger.error(f"Activity log failed: {log_error}")

            finally:
                db.close()

        return response

