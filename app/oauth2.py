from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from .config import settings

from sqlalchemy.orm import Session

from . import schemas, database, models, utils

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(id: int):
    db = database.SessionLocal()

    user_query = db.query(models.Users).filter(models.Users.id == id)

    if user_query.first():
        return user_query.first()

def get_user_username(email: str):
    db = database.SessionLocal()

    user_query = db.query(models.Users).filter(models.Users.email == email)

    if user_query.first():
        return user_query.first()

def authenticate_user(email:str, password:str):
    user = get_user_username(email)
    if not user:
        return False
    if not utils.verify_password(password, user.password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    user = get_user(id)
    if user is None:
        raise credentials_exception
    return user
    

def get_current_active_user(current_user: schemas.UserOut = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user