
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import os
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

class JWTAthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
       if request.url.path in ["/","/login", "/signup","/docs", "/openapi.json"]:
           return await call_next(request)
       auth_header = request.headers.get('Authorization')
       if auth_header is None or not auth_header.startswith('Bearer '):
           raise HTTPException(status_code=401, detail="Unauthorized")
       token= auth_header.replace('Bearer ', '')
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
           request.state.user = payload.get("sub")
       except jwt.ExpiredSignatureError:
           raise HTTPException(status_code=401, detail="Token has expired")
       except jwt.InvalidTokenError:
           raise HTTPException(status_code=401, detail="Invalid token")
       
       return await call_next(request)