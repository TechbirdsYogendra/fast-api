from fastapi import APIRouter, Path, Query, status

from app.core.deps import CurrentUser, DbSession
from app.core.responses import api_response
from app.models import AuthorRecord, BookRecord
from app.schemas.book import BookCreate

router = APIRouter(tags=["books"])


def owned_book(db: DbSession, book_id: int, user_id: int):
    return db.query(BookRecord).filter(
        BookRecord.id == book_id,
        BookRecord.user_id == user_id,
    ).first()


@router.get("/books")
def get_books(db: DbSession, current_user: CurrentUser):
    books = db.query(BookRecord).filter(BookRecord.user_id == current_user.id).all()
    return [book.to_dict() for book in books]


@router.post("/books")
def create_book(create_book: BookCreate, db: DbSession, current_user: CurrentUser):
    author = AuthorRecord(
        f_name=create_book.author.fName,
        l_name=create_book.author.lName,
        bio=create_book.author.bio,
    )
    db.add(author)
    db.flush()
    book = BookRecord(
        title=create_book.title,
        description=create_book.description,
        rating=create_book.rating,
        author_id=author.id,
        user_id=current_user.id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return api_response(
        status.HTTP_201_CREATED, True, "Book created", book.to_dict()
    )


@router.get("/books/{book_id}")
def get_book(db: DbSession, current_user: CurrentUser, book_id: int = Path(ge=1)):
    book = owned_book(db, book_id, current_user.id)
    if book is None:
        return api_response(status.HTTP_404_NOT_FOUND, False, "Book not found")
    return api_response(status.HTTP_200_OK, True, "Book found", book.to_dict())


@router.put("/books/{book_id}")
def update_book(
    update_book: BookCreate,
    db: DbSession,
    current_user: CurrentUser,
    book_id: int = Path(ge=1),
):
    book = owned_book(db, book_id, current_user.id)
    if book is None:
        return api_response(status.HTTP_404_NOT_FOUND, False, "Book not found")
    book.title = update_book.title
    book.description = update_book.description
    book.rating = update_book.rating
    db.commit()
    db.refresh(book)
    return api_response(status.HTTP_200_OK, True, "Book updated", book.to_dict())


@router.delete("/books/{book_id}")
def delete_book(db: DbSession, current_user: CurrentUser, book_id: int = Path(ge=1)):
    book = owned_book(db, book_id, current_user.id)
    if book is None:
        return api_response(status.HTTP_404_NOT_FOUND, False, "Book not found")
    db.delete(book)
    db.commit()
    return api_response(status.HTTP_200_OK, True, "Book deleted")


@router.get("/books/")
def get_books_by_author(
    db: DbSession,
    current_user: CurrentUser,
    author: str = Query(min_length=3, max_length=50),
):
    books = (
        db.query(BookRecord)
        .join(AuthorRecord)
        .filter(
            BookRecord.user_id == current_user.id,
            (AuthorRecord.f_name == author) | (AuthorRecord.l_name == author),
        )
        .all()
    )
    if not books:
        return api_response(status.HTTP_404_NOT_FOUND, False, "Book not found")
    return api_response(
        status.HTTP_200_OK,
        True,
        "Book found",
        [book.to_dict() for book in books],
    )
