from fastapi import APIRouter, Body, HTTPException, Path, status

from app.core.deps import CurrentUser, DbSession
from app.models import Todo
from app.schemas.todo import TodoCreate

router = APIRouter(tags=["todos"])


@router.get("/todos", status_code=status.HTTP_200_OK)
def get_todos(db: DbSession, current_user: CurrentUser):
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()


@router.get("/todos/{todo_id}")
def get_todo(db: DbSession, current_user: CurrentUser, todo_id: int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: DbSession, current_user: CurrentUser):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        priority=todo.priority,
        user_id=current_user.id,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def update_todo(
    db: DbSession,
    current_user: CurrentUser,
    todo_id: int = Path(gt=0),
    todo: TodoCreate = Body(),
):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    db_todo.priority = todo.priority
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: DbSession, current_user: CurrentUser, todo_id: int = Path(gt=0)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
