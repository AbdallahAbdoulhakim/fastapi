from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, auth, posts, votes
from . import models, database

from .config import settings

# not needed anymore because alembic is set

#models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins=["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def welcome():
    return {"result":"Welcome to the API!"}

app.include_router(users.root)
app.include_router(auth.root)
app.include_router(posts.root)
app.include_router(votes.root)


