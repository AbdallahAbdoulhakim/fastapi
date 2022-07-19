from fastapi import APIRouter, FastAPI, Depends, HTTPException, Response, status
from .. import schemas, oauth2, database, models
from sqlalchemy.orm import Session

root=APIRouter(prefix="/votes", tags=["Votes"])

@root.post("/", status_code=status.HTTP_204_NO_CONTENT)
def vote(vote: schemas.Vote, current_user: schemas.UserOut = Depends(oauth2.get_current_active_user), 
db: Session = Depends(database.get_db)):

    post = db.query(models.Posts).filter(models.Posts.id == vote.id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

    vote_query = db.query(models.Votes).filter(models.Votes.owner_id == current_user.id, models.Votes.post_id == vote.id)

    
    if not vote_query.first():
        if vote.dir == schemas.VoteDir.cancelVote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post has not been liked!")

        vote_created = models.Votes(owner_id=current_user.id, post_id=vote.id)
        db.add(vote_created)

    else:
        if vote.dir == schemas.VoteDir.UpVote :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post already liked!")

        db.delete(vote_query.first())

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)