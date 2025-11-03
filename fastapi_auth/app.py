# FastAPI with SQL Integration

# CRUD Operations / HTTP Requests

# Create - POST
# Read - GET
# Update - PUT
# Delete - DELETE

# uvicorn [app .py script name]:app --reload        ––no need to include "[]" with .py name

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Integration with SQL")



#                                      ---DATABASE SETUP---


# database setup -> connecting to a file

# ->entry point for your database<-
engine = create_engine("sqlite:///dev.db", connect_args={"check_same_thread" : False}) 

# connect_args={"check_same_threade":False} -> makes SQL keep up with FastAPI's multiple threads

# autocommit=False, autoflush=False help not reload the db engine everytime fastapi reloads
# bind=engine connects SessionLocal to engine (the db engine above)

# ->Session Factory<-
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A session is an object that acts as a TEMPORARY WORKSPACE for your database operations.

# By default, SQLite only allows one thread to interact with it to prevent data corruption
# FastAPI is asynchronous and handles requests in a thread pool (meaning multiple threads are used)
# Without this flag, any request that isn't the very first one would fail, claiming the database is "locked by another thread"
# Other databases (like PostgreSQL) don't need this.

# ->creates the base class that our database models will inherit from<-
Base = declarative_base()




#                                      ---DATABASE MODEL---




# database model -> The structure of your users table in SQL, represented as a Python class
class User(Base):
    __tablename__ = "users" # ORM model -> maps Python User class directly to the SQL users table 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(100), nullable=False)
 
 
 
 
#                                      ---TABLE CREATION---
 
   
# Tell the engine to create all tables defined by 'Base' (i.e, the 'users' table)
Base.metadata.create_all(engine)

# Base.metadata has been collecting all the table definitions (like User). This line tells the engine
# to connect to the database and run the "CREATE TABLE IF NOT EXISTS ..." command for *all*
# the tables it knows about



#                                      ---PYDANTIC MODELS---


# Pydantyc models (Dataclass)
# API models; the shape of the data your API will input and output


# *** Why two models? ***
# This is a critical security and design pattern

# UserCreate -> the input model
# A client creating a user should only send a name, email, and role. They should *not* send an id.

# UserResponse -> this is the output model
# When you send a user back to the client, you do want to include the id.

# model_config = {"from_attributes" : True}
# This is what allows you to take a SQLAlchemy User object (which uses attributes) 
# and directly convert it into a UserResponse model

class UserCreate(BaseModel):
    name:str
    email:str
    role:str
    
class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    role:str

    model_config = {"from_attributes" : True}


   
#                                      ---Dependency Injection---


# What it is? -> A generator that treats and cleans up a database session for each request.
# Why? -> You *MUST* have a separate, new session for every single API request. 
# You cannot share one global session. This get_db function is the standard FastAPI pattern to 
# manage this.

# This pattern is essential for 2 reasons: 1. COncurrency and Error Handling


# Session Management -> The system for handling database connections safely for each API request     
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
     