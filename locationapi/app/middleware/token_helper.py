from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from app.schema import LoginRequest
from app.models import Location
security_scheme = HTTPBearer()
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

def create_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):    
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    
def get_current_user( credentials: HTTPAuthorizationCredentials = Depends(security_scheme),):
    token = credentials.credentials
    payload = decode_token(token)
    return payload

def verify_login_credentials(file_path: str, login_request:LoginRequest) -> bool:
    # For demonstration purposes, using hardcoded credentials
    # In production, verify against a user database
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            _, username, password = line.strip().split(',')
            if login_request.username == username and login_request.password == password:
                return True
    return False

def audit_log(location:Location):
     with open("location_audit.log", "a", encoding="utf-8") as f:
        f.write(f"Location created: {location.code},{location.name},{location.latitude},{location.longitude}\n")