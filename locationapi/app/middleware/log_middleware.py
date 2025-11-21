from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        # ---- Log Incoming Request ----
        print("\n================ REQUEST ================")
        print(f"Method     : {request.method}")
        print(f"URL        : {request.url}")
        print(f"Headers    : {dict(request.headers)}")

        # Read request body (must read & replace stream)
        body_bytes = await request.body()
        if body_bytes:
            print(f"Body       : {body_bytes.decode('utf-8', errors='ignore')}")

        # Pass request to next handler
        response = await call_next(request)

        # ---- Log Response ----
        duration = round((time.time() - start_time) * 1000, 2)
        print("\n================ RESPONSE ===============")
        print(f"Status Code: {response.status_code}")
        print(f"Time Taken : {duration} ms")
        print("========================================\n")

        return response
        
    