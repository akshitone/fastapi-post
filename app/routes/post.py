from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response, status


from app import models, schemas  # import all models and schemas
from app.database import get_db

router = APIRouter()


@router.get('/api/v1/posts', status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse], tags=["Post"])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/api/v1/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse, tags=["Post"])
# def create_post(request: dict = Body(...)): # when you don't know what data you're expecting
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())  # unpack the post into a dict
    db.add(new_post)  # create a new post object
    db.commit()  # commit to the database
    db.refresh(new_post)  # refresh the new post with id and created_at fields
    return new_post


@router.get('/api/v1/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse, tags=["Post"])
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete('/api/v1/posts/{id}', tags=["Post"])
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/api/v1/posts/{id}', response_model=schemas.PostResponse, tags=["Post"])
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post.first()
