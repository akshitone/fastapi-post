from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status


from app import models, schemas  # import all models and schemas
from app.database import get_db
from app.utils import hashing_password

router = APIRouter()


@router.post('/api/v1/users/sign-up',  status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse, tags=["User"])
def sign_up(user: schemas.User, db: Session = Depends(get_db)):
    existed_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    if existed_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")

    # hash password for authentication
    user.password = hashing_password(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
