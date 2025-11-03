# Te quedaste en 12:48 en los pydantic models

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List
from passlib.context import CryptContext
import jwt


#                                      ---Security Configuration---
SECRET_KEY = "sicccccccapp"
ALGORITHM = "HS256"
TOKEN_EXPIRES = 30 # Usually is 30 minutes

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



app = FastAPI(title="Integration with SQL and OAuth")



#                                      ---DATABASE SETUP---
engine = create_engine("sqlite:///dev.db", connect_args={"check_same_thread" : False}) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#                                      ---DATABASE MODEL---
class User(Base):
    __tablename__ = "users" # ORM model -> maps Python User class directly to the SQL users table 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(100), nullable=False)
    hashed_pwd = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
 
#                                      ---TABLE CREATION---
Base.metadata.create_all(engine)

#                                      ---PYDANTIC MODELS---
class UserCreate(BaseModel):
    name:str
    email:str
    role:str
    password:str
    
class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    role:str
    is_active = bool

    model_config = {"from_attributes" : True}
    
class UserLogin(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData():
    email: str | None = None




#                                      ---Dependency Injection---
def get_db():
    db = SessionLocal() # Creates a new session
    try:
        yield db # Provide the session to the endpoint
    finally:
        db.close() # Close the session after the request is done
        


#                                                       ---Endpoints---
@app.get("/")
def root():
    return {"message" : "Intro to FastAPI with SQL"}


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    return user


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="User already exists!")
    
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist!")
    
    for field, value in user.dict().items():
        setattr(db_user, field, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user
    

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist!")
    
    
    db.delete(db_user)
    db.commit()
    
    return {"message" : "User deleted!"}


@app.get("/get_all_users/", response_model=UserResponse)
def get_all(db: Session = Depends(get_db)):
    users = db.query(User).all()
    
    if not users:
        HTTPException(status_code=404, detail="No users on database!")
        
    return users
     