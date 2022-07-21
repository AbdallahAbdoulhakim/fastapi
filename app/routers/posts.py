from typing import List, Optional 
from fastapi import APIRouter, Depends, HTTPException, Response, status
from .. import schemas, oauth2, database, models
from sqlalchemy.orm import Session
from sqlalchemy import func

root = APIRouter(prefix="/posts", tags=["Posts"])


# CRUD OPERATIONS

# READ ALL
@root.get("/", response_model=List[schemas.Post])
def get_posts(search:Optional[str]="", limit:int = 10, skip:int = 0, current_user: schemas.UserOut = Depends(oauth2.get_current_active_user), 
db: Session = Depends(database.get_db)):
    posts = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Posts.id == models.Votes.post_id, isouter = True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# READ ONE

@root.get("/{id}", response_model=schemas.Post)
def get_post(id:int, current_user: schemas.UserOut = Depends(oauth2.get_current_active_user), 
db: Session = Depends(database.get_db)):

    post = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).filter(models.Posts.id == id).join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    
    return post

# CREATE

@root.post("/", response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.BasePost, current_user: schemas.UserOut = Depends(oauth2.get_current_active_user), 
db: Session = Depends(database.get_db)):


    post_created = models.Posts(**post.dict(), owner_id=current_user.id)

    db.add(post_created)
    db.commit()
    db.refresh(post_created)    

    return post_created


# UPDATE 

@root.put("/{id}")
def update_post(id:int, post:schemas.BasePost, current_user: schemas.UserOut = Depends(oauth2.get_current_active_user), 
db: Session = Depends(database.get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized action!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


# DELETE 

@root.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id:int, current_user: schemas.UserOut = Depends(oauth2.get_current_active_user), 
db: Session = Depends(database.get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized action!")

    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

