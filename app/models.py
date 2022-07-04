from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text

from .database import Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
