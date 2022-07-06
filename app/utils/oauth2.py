from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.models import schemas, models
from app.models.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

SECRET_KEY = '32db07e92de9ba3f3e7281e12ee1dd13947f4acc3f449aeb876cc7f195aa51a8'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"expire_time": expire_time.timestamp()})
        encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_token

    except JWTError as error:
        print("Error while creating access token:", error)


def verify_token(token: str, credentials_exception):
    try:
        user_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = user_data.get('user_id')

        if not id:
            raise credentials_exception

        token_data = schemas.TokenRequest(id=id)
        return token_data

    except JWTError as error:
        print("Error while verifying token:", error)
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_token(token, credentials_exception)

    user = db.query(models.User).filter(
        models.User.id == token_data.id).first()

    return user
