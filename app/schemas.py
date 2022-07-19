from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class VoteDir(Enum):
    UpVote=1
    cancelVote=0


class BaseUser(BaseModel):
    email:str
    disabled:bool = False

class UserCreate(BaseUser):
    password:str

class UserOut(BaseUser):
    id:int
    created_at:datetime

    class Config:
        orm_mode = True

class BasePost(BaseModel):
    title:str
    content:str

class PostOut(BasePost):
    id:int
    created_at:datetime
    owner:UserOut

    class Config:
        orm_mode = True

class Post(BaseModel):
    Posts:PostOut
    votes:int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    id:int
    dir:VoteDir

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int

