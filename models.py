from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    image_name = Column(String, nullable=False)
    image_uploaded_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, nullable=False, primary_key=True)
    comment = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, nullable=False, primary_key=True)
    likes = Column(Integer, default=0)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
