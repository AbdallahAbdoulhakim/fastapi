from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, utils, database, models, oauth2


root = APIRouter(prefix="/users", tags=["Users"])


@root.post("/", response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(database.get_db)):
    user.password = utils.get_password_hash(user.password)
    user_query = db.query(models.Users).filter(models.Users.email == user.email)

    if user_query.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user.email} already exists!")

    user_created = models.Users(**user.dict())

    db.add(user_created)
    db.commit()
    db.refresh(user_created)

    return user_created

@root.get("/me", response_model=schemas.UserOut)
async def read_users_me(current_user: schemas.UserOut = Depends(oauth2.get_current_active_user)):
    return current_user