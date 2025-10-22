# CRUD -> Create Read Update Delete

# HTTP Requests -> GET PUT POST DELETE

# These request correspond to CRUD
# Create -> POST
# Read -> GET
# Update -> PUT
# Delete -> DELETE

# to run the app, write in the terminal uvicorn [name of .py file]:app --reload
# reload ensures that everytime you make a change, it automatically reloads for you

# http://127.0.0.1:8000/docs#/

from fastapi import FastAPI, HTTPException, status, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

# In the real world you would use postgres, mongodb
users = {
    1 : {
        "name" : "Gabs",
        "website" : "google.com/",
        "role" : "Developer"        
    }
}


# Base Pydantic models
class User(BaseModel):
    name: str
    website: str
    role: str

class UpdateUser(BaseModel):
    name: str | None = None
    website: str | None = None
    role: str | None = None
    


# Endpoint; simply put it's like an URL
@app.get("/")
def root():
    # Data is passed through the API typically through JSON
    return {"message" : "Welcome to your introduction to FastAPI"} # python dictioonaries are similar to JSON


# Get a user
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., description="The ID you want to GET", gt=0, lt=100)): # gt -> greater than, lt -> less than
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found!")
    return users[user_id]


# Create User
@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED) # a 201 status means we've successfully created
def create_user(user_id: int, user: User):
    if user_id in users:
        raise HTTPException(status_code=400, detail="User already exists!")
    
    users[user_id] = user.dict()
    return user


# Update User
@app.put("/users/{user_id}")
def update_user(user_id:int, user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found!")
    
    current_user = users[user_id]
    
    if user.name is not None:
        current_user["name"] = user.name
    
    if user.website is not None:
        current_user["website"] = user.website
    
    if user.role is not None:
        current_user["role"] = user.role
    
    return current_user

# Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found!")
    
    deleted_user = users.pop(user_id)
    
    return {
        "message" : "User has benn deleted", 
        "deleted_user" : deleted_user
    }

# Search User
@app.get("/users/search/")
def search_by_name(name: str | None = None):
    if not name:
        raise {"message" : "Name parameter is required!"}
    
    for user in users.values():
        if user["name"] == name:
            return user
    
    raise HTTPException(satatus_code=404, detail="User not found!")