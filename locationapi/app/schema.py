from pydantic import BaseModel

class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    created_on: str  # ISO format date string

class LocationCreate(LocationBase):
    pass

class LocationUpdate(LocationBase):
    pass

class LocationNameUpdate(BaseModel):
    name: str

class LocationDelete(LocationBase):
    pass
class LocationOut(LocationBase):
    code: int

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"