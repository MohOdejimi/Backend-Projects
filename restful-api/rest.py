from fastapi import FastAPI, HTTPException
from typing import Any

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "year": 1958,
        "genre": "Historical Fiction",
        "available": True
    },
    {
        "id": 2,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937,
        "genre": "Fantasy",
        "available": True
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian",
        "available": False
    },
    {
        "id": 4,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "genre": "Classic",
        "available": True
    },
    {
        "id": 5,
        "title": "Half of a Yellow Sun",
        "author": "Chimamanda Ngozi Adichie",
        "year": 2006,
        "genre": "Historical Fiction",
        "available": True
    },
    {
        "id": 6,
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "genre": "Science Fiction",
        "available": False
    },
    {
        "id": 7,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "year": 1813,
        "genre": "Romance",
        "available": True
    },

]


# READ
@app.get("/")
def getBooks():
    return books 

# GET ONE BOOK 
@app.get('/{id}')
def getOneBook(id):
    for book in books:
        if book["id"] == int(id):
            return book

    raise HTTPException(status_code=404, detail="Book not found")

# CREATE 
@app.post('/book')
def createBook(book: dict[str, Any]):
    new_id = max(book["id"] for book in books) + 1 
    book["id"] = new_id
    books.append(book)
    return book

# UPDATE 
@app.put("/book/{id}")
def updateBook(id: str, updated_book: dict[str, Any]):
    for book in books:
        if book["id"] == int(id):
            updated_book["id"] = id 
            book = updated_book
        

# DELETE 
@app.delete('/book/{id}')
def deleteBook(id):
    for book in books:
        if book["id"] == int(id):
            books.remove(book)
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")
