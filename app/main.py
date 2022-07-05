from fastapi import FastAPI

from app import models  # import all models and schemas
from app.database import engine
from app.routes import post, user

# for database compatibility with sqlalchemy
# will create tables using models if doesn't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API for Post and User Management",
    description="Using postgresql and sqlalchemy ORM to manage database and pydantic for schemas",
    version="0.0.1",
)

app.include_router(post.router)  # included post router
app.include_router(user.router)  # included user router


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
