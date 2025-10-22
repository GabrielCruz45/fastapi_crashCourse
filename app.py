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

# Endpoint; simply put it's like an URL
@app.get("/")
def root():
    # Data is passed through the API typically through JSON
    return {"message" : "Welcome to your introduction to FastAPI"} # python dictioonaries are similar to JSON