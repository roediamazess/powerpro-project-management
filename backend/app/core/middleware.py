import time
import json
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

class AuditLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware to intercept and log requests. 
    Note: For complex Audit Logs (old vs new payload), 
    this should be paired with SQLAlchemy Event Listeners.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # We only care about mutations for audit logs generally
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            # Logic to capture request body could go here
            # But be careful with reading stream twice
            pass

        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
