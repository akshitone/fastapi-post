from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status


from app.models import schemas, models  # import all models and schemas
from app.models.database import get_db
from app.utils.utils import verify_password
from app.utils.oauth2 import create_access_token

router = APIRouter(
    prefix='/api/v1/auth',
    tags=["Auth"]
)


@router.post('/login', response_model=schemas.Token, status_code=status.HTTP_200_OK)
def login(user: schemas.User, db: Session = Depends(get_db)):
    existed_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    if not existed_user or not verify_password(user.password, existed_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Incorrect username or password")

    access_token = create_access_token(data={"user_id": existed_user.id})

    return {"access_token": access_token, "token_type": "bearer"}
