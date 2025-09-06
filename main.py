from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field

import models
from database import Base, engine, SessionLocal

# ---------- DB Setup ----------
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore REST API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Schemas ----------
class BookCreate(BaseModel):
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=1, ge=0)

class BookOut(BookCreate):
    id: int
    class Config:
        orm_mode = True

# ---------- CRUD Endpoints ----------
@app.post("/books/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, data: BookCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in data.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

@app.get("/search/", response_model=List[BookOut])
def search_books(q: str, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.title.ilike(f"%{q}%")).all()

# ---------- Root Endpoint ----------
@app.get("/")
def root():
    return {"message": "Welcome to the Bookstore API"}

# ---------- Startup Event: Insert Sample Books ----------
@app.on_event("startup")
def add_sample_books():
    db = SessionLocal()
    sample_books = [
        {"title": "Python Basics", "author": "John Doe", "price": 299.99, "quantity": 5},
        {"title": "FastAPI Guide", "author": "Jane Smith", "price": 399.99, "quantity": 3},
        {"title": "Data Science 101", "author": "Alice Brown", "price": 499.99, "quantity": 7}
    ]
    for book in sample_books:
        exists = db.query(models.Book).filter(models.Book.title == book["title"]).first()
        if not exists:
            db_book = models.Book(**book)
            db.add(db_book)
    db.commit()
    db.close()
