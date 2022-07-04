from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):  # Post class model for post
    title: str
    description: str
    published: bool = False  # False by default
    rating: Optional[float] = None  # Optional: None by default


while True:
    try:
        connection = psycopg2.connect(host='172.17.0.2', database='fastapi_post_db',
                                      user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection established")
        break
    except Exception as error:
        print("Error connecting to database: ", error)
        time.sleep(2)


posts = [
    {"title": "My Projects 01", "description": "This is a project that contains a list of projects",
        "published": True, "rating": 4.5, "id": 123},
    {"title": "My Projects 02", "description": "This is a project that contains a list of projects that are published",
        "published": True, "rating": 4.2, "id": 125},
    {"title": "My Projects 03", "description": "This is a project", "id": 127},
]


def find_post(id):
    founded_post = {}
    for post in posts:
        if post['id'] == id:
            founded_post = post
            break

    return founded_post


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
def get_posts():
    return {"data": posts}


@app.post('/api/v1/posts', status_code=status.HTTP_201_CREATED)
# def create_post(request: dict = Body(...)): # when you don't know what data you're expecting
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    posts.append(post_dict)
    return {"data": post_dict}


@app.get('/api/v1/post/{id}')
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": "Post not found"})  # Exception message for missing post object
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post not found"}

    return {"data": post}
