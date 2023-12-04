from . import db
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(Text, nullable=False)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'<User: {self.username}>'

class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[bool] = mapped_column(Boolean, default=False)

    def __init__(self, created_by, title, description, status = False) -> None:
        self.created_by = created_by
        self.title = title
        self.description = description
        self.status = status

    def __repr__(self) -> str:
        return f'<Todo: {self.title}>'