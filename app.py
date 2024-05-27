import numpy as np
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File,status
import uvicorn
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from face import detect_face
import cv2
from tempfile import NamedTemporaryFile
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from utils import get_hashed_password,verify_password,create_access_token,create_refresh_token
from cachetools import cached, TTLCache




app = FastAPI() # Creating an instance of FastAPI
models.Base.metadata.create_all(bind=engine) # Creating all tables in the database using SQLAlchemy models

cache = TTLCache(maxsize=100, ttl=300) # Creating a cache with a maximum size of 100 items and a time-to-live of 300 seconds

# Function to generate a cache key from arguments
def get_cache_key(*args, **kwargs):
    return str(args) + str(kwargs)

# Dependency that provides a SQLAlchemy session and ensures it's closed after the request
def get_db():   
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Pydantic model for user data validation
class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=5, max_length=50)


# Pydantic model for token data validation
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

# Setting up OAuth2 with password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# List to store users
users = []

  
def authenticate_user(name: str, password: str,db: Session=Depends(get_db)): # Function to authenticate a user
    user = db.query(models.User).filter(func.lower(models.User.name) == func.lower(name)).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


@app.get("/", summary="Root endpoint",) # Root endpoint for testing or API index
async def root(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    user_names = [user.name for user in users]
    return {"user_names": user_names}
    


@app.post("/create",summary="Create new user") # Endpoint to create a new user
def create_user(user: User, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.name = user.name 
    user_model.password = get_hashed_password(user.password)
    print("Adding user")
    db.add(user_model)
    db.commit()
    print("User added")

    return user_model

@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema) # Endpoint to login and create tokens
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token = create_access_token(user.name)
    refresh_token = create_refresh_token(user.name)
    return {"access_token": access_token, "refresh_token": refresh_token}



@app.put("/{user_id}")  # Endpoint to update a user by ID
@cached(cache, key=get_cache_key)
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404, detail=f"ID {user_id} : Does not exist in database"
        )

    user_model.name = user.name

    db.add(user_model)
    db.commit()

    return user



@app.post("/search")  # Endpoint to search users by name
def search_by_name(name_to_search: str, user: User, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.name == name_to_search).all()
    user_model = (
        db.query(models.User)
        .filter(func.lower(models.User.name).like(func.lower(f"%{name_to_search}%")))
        .all()
    )

    if user_model is None:
        raise HTTPException(
            status_code=404, detail=f"User with name '{name_to_search}' not found"
        )

    return user_model


# Endpoint to process uploaded images and detect faces
@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result_image, cropped_face = detect_face(image)

        temp_file = NamedTemporaryFile(delete=False, suffix=".jpg")
        cv2.imwrite(temp_file.name, result_image)
        cv2.imwrite(temp_file.name, cropped_face)

        return FileResponse(temp_file.name, media_type="image/jpeg")

    except Exception as e:
        return {"error": str(e)}

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)