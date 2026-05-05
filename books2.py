from typing import Optional
from fastapi import FastAPI , Path ,Query ,HTTPException
from pydantic import BaseModel,Field
from starlette import status

app = FastAPI()

class Book :
    id : int
    title : str 
    author : str
    description : str
    rating : int
    published_date: int

    def __init__(self,id,title,author,description,rating,published_date) :
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel) :
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_len =3)
    author : str = Field(min_len =1)
    description : str = Field(min_len =1 , max_length= 100 )
    rating : int  = Field(gt = 0 , lt = 6)
    published_date : int = Field(gt = 0 , lt = 2027)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"a new book",
                "author":"random author",
                "description":"random description of a book",
                "rating":5,
                "published_date":2026

            }
        }
        
    }

books = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "A story of wealth and obsession in the Jazz Age.", 5 , 2002),
    Book(2, "1984", "George Orwell", "A dystopian novel about totalitarianism and surveillance.", 5 , 2001),
    Book(3, "To Kill a Mockingbird", "Harper Lee", "A powerful story of racial injustice in the American South.", 4 , 2014),
    Book(4, "The Hobbit", "J.R.R. Tolkien", "A fantasy adventure about a hobbit on a quest.", 5 , 2018),
    Book(5, "Atomic Habits", "James Clear", "A guide to building good habits and breaking bad ones.", 4 , 2024),
    Book(6, "cooking for omar", "omar", "a book about cooking", 5 , 2001)
]




@app.get("/books",status_code=status.HTTP_200_OK) # this is the path to get all books
async def read_all_books():
    return books

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def search_book_by_id(book_id:int = Path(gt = 0)):
    for book in books :
        if book.id == book_id :
            return book
    raise HTTPException(status_code=404,detail = 'Item not found')


@app.get("/books/",status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating_value:int = Query(gt=0 ,lt=6)):
    books_to_return = []
    for book in books :
        if book.rating == rating_value :
            books_to_return.append(book)
    return books_to_return

@app.get("/books/published/",status_code=status.HTTP_200_OK)
def get_books_by_published_date(date : int =Query(gt = 0 , lt = 2027)):
    books_to_return = []
    for book in books :
        if book.published_date == date :
            books_to_return.append(book)
    return books_to_return

@app.post("/create_book",status_code = status.HTTP_201_CREATED) # this is the path to create a new book
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(find_book_id(new_book))


def find_book_id(book : Book):
    book.id = 1 if len(books) == 0 else books[-1].id +1
    return book
    

@app.put("/book/update_book",status_code= status.HTTP_204_NO_CONTENT)
async def update_book(book : BookRequest):
    book_changed = False
    for i in range(len(books)) :
        if books[i].id == book.id :
            books[i] = book
            book_changed = True
    if not book_changed :
        raise HTTPException(status_code=404,detail='Item not found')


@app.delete("/book/{book_id}",status_code= status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int = Path(gt=0)):
    book_changed = False
    for i in range(len(books)):
        if book_id == books[i].id :
            books.pop(i)
            book_changed = True
            break
    if not book_changed :
        raise HTTPException(status_code=404 , detail = 'Item not found')