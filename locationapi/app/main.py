import http
from sqlalchemy import create_engine

from fastapi import FastAPI
from app.database import Base, engine, get_db
from app.middleware.log_middleware import LoggingMiddleware
from app.middleware.jwtauth import JWTAthenticationMiddleware
from app.middleware.token_helper import audit_log, create_token, get_current_user, verify_login_credentials
from app.models import Location
from app.schema import LocationCreate, LocationNameUpdate, LocationOut, LoginRequest, TokenResponse
from sqlalchemy.orm import Session
from fastapi import Depends,status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uvicorn

# Create the database tables
Base.metadata.create_all(bind=engine)

#create fastapi app
app = FastAPI()
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
#add middleware
app.add_middleware(JWTAthenticationMiddleware)
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def load_home():
    return {"message": "Welcome to the Location API"}


@app.post("/login", response_model=TokenResponse)
def jwt_login(login_request:LoginRequest):
    CSV_PATH = Path(__file__).resolve().parent.parent / "app/users.csv"
    if not verify_login_credentials(CSV_PATH, login_request):
         return status.HTTP_401_UNAUTHORIZED
    else:
      access_token = create_token(data={"sub": login_request.username})
      return {"access_token": access_token, "token_type": "bearer"}

@app.post("/locations/v1.0/", response_model=LocationOut, status_code=status.HTTP_201_CREATED,dependencies=[Depends(get_current_user)])
def create_location(location:LocationCreate,background_tasks: BackgroundTasks, db:Session=Depends(get_db)):
    db_location = Location(name=location.name, latitude=location.latitude, longitude=location.longitude, created_on=location.created_on)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    background_tasks.add_task(audit_log, db_location)
    return db_location

@app.get("/locations/v1.0/", response_model=list[LocationOut],dependencies=[Depends(get_current_user)])
def get_locations(db:Session=Depends(get_db)):
    locations = db.query(Location).all()
    return locations
@app.get("/locations/v1.0/{code}", response_model=LocationOut)
def get_location_by_code(code:int, db:Session=Depends(get_db)):
    return db.query(Location).filter(Location.code==code).first()

@app.get("/locations/v1.0/name/{name}", response_model=list[LocationOut])
def get_location_by_name(name:str, db:Session=Depends(get_db)):
    return db.query(Location).filter(Location.name==name).all()

@app.patch("/locations/v1.0/{code}", response_model=LocationOut)
def update_location(code:int, location:LocationNameUpdate, db:Session=Depends(get_db)):
    db_location = db.query(Location).filter(Location.code==code).first()
    if db_location:
        db_location.name = location.name        
        db.commit()
        db.refresh(db_location)
    return db_location
@app.delete("/locations/v1.0/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(code:int, db:Session=Depends(get_db)):
    db_location = db.query(Location).filter(Location.code==code).first()
    if db_location:
        db.delete(db_location)
        db.commit()
    return None


if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=9000)