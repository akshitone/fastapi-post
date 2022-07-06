from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response, status


from app.models import schemas, models  # import all models and schemas
from app.utils.oauth2 import get_current_user
from app.models.database import get_db

router = APIRouter(
    prefix='/api/v1/posts',
    tags=["Post"]
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse])
# Depends(get_current_user) automatically check for user is logged in or not with verifying the token
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#   posts = db.query(models.Post).filter(
#       models.Post.user_id == current_user.id).all()  # get all posts of current user only
def get_posts(db: Session = Depends(get_db), limit: int = 5, offset: int = 0):
    posts = db.query(models.Post).limit(limit).offset(offset).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# def create_post(request: dict = Body(...)): # when you don't know what data you're expecting
# get_current_user is used to verify token validation
# it will added to every request where you expect authorization
# if token is not present, create post return 401
def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # unpack the post into a dict
    # getting id from the token
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)  # create a new post object
    db.commit()  # commit to the database
    db.refresh(new_post)  # refresh the new post with id and created_at fields
    return new_post


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # check the post is related to the current user with token
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Post unauthorized")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # check the post is related to the current user with token
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Post unauthorized")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post
