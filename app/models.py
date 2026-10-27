from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class AuthorRecord(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    f_name = Column(String(50), nullable=False)
    l_name = Column(String(50), nullable=False)
    bio = Column(String(300), nullable=False)
    books = relationship("BookRecord", back_populates="author")


class BookRecord(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    rating = Column(Float, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    author = relationship("AuthorRecord", back_populates="books")
    owner = relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "rating": self.rating,
            "author": {
                "fName": self.author.f_name,
                "lName": self.author.l_name,
                "bio": self.author.bio,
            },
        }


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    completed = Column(Boolean, default=False)
    priority = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    hashed_password = Column(String(255), nullable=False)
