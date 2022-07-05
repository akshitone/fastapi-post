from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status


from app.models import schemas, models  # import all models and schemas
from app.models.database import get_db
from app.utils.utils import hashing_password, verify_password

router = APIRouter(
    prefix='/api/v1/auth',
    tags=["Auth"]
)


@router.post('/login')
def login(user: schemas.User, db: Session = Depends(get_db)):
    existed_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    if not existed_user or not verify_password(user.password, existed_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    return {"message": "Successfully authenticated"}
