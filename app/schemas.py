from pydantic import BaseModel


class Post(BaseModel):  # Post class model for post
    title: str
    content: str
    published: bool = False  # False by default
