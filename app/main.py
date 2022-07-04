
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response, status

from . import models  # import all models
from .database import engine, get_db
from .schemas import Post

# for database compatibility with sqlalchemy
# will create tables using models if doesn't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# this is a dectorator that turns the functions into actual path operations
# http methods GET, POST, PUT, DELETE
@app.get("/")  # route to fast API endpoint
def root():
    return {"message": "Hello World"}

# @ - decorator for fast API
# app - fast API instance
# get - http methods
# root - fast API functions

# when we hit endpoint. it goes down top to bottom and search for matching api endpoint.
# and stops when first match.
# order matters


@app.get('/api/v1/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post('/api/v1/posts', status_code=status.HTTP_201_CREATED)
# def create_post(request: dict = Body(...)): # when you don't know what data you're expecting
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())  # unpack the post into a dict
    db.add(new_post)  # create a new post object
    db.commit()  # commit to the database
    db.refresh(new_post)  # refresh the new post with id and created_at fields
    return {"data": new_post}


@app.get('/api/v1/posts/{id}', status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": post}


@app.delete('/api/v1/posts/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/api/v1/posts/{id}')
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post.first()}
