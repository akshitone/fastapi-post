from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Path, Response, status


from app import models, schemas  # import all models and schemas
from app.database import engine, get_db
from app.utils import hashing_password

# for database compatibility with sqlalchemy
# will create tables using models if doesn't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API for Post and User Management",
    description="Using postgresql and sqlalchemy ORM to manage database and pydantic for schemas",
    version="0.0.1",
)


# this is a dectorator that turns the functions into actual path operations
# http methods GET, POST, PUT, DELETE
@app.get("/", tags=["Test"])  # route to fast API endpoint
def root():
    return {"message": "Hello World"}

# @ - decorator for fast API
# app - fast API instance
# get - http methods
# root - fast API functions

# when we hit endpoint. it goes down top to bottom and search for matching api endpoint.
# and stops when first match.
# order matters


@app.get('/api/v1/posts', status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse], tags=["Post"])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/api/v1/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse, tags=["Post"])
# def create_post(request: dict = Body(...)): # when you don't know what data you're expecting
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())  # unpack the post into a dict
    db.add(new_post)  # create a new post object
    db.commit()  # commit to the database
    db.refresh(new_post)  # refresh the new post with id and created_at fields
    return new_post


@app.get('/api/v1/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse, tags=["Post"])
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@app.delete('/api/v1/posts/{id}', tags=["Post"])
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/api/v1/posts/{id}', response_model=schemas.PostResponse, tags=["Post"])
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post.first()


@app.post('/api/v1/users/sign-up',  status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse, tags=["User"])
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
