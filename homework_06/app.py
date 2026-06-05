import json
import os

from flask import Flask, render_template, request

app = Flask(__name__)

FILE = "books.json"


def load_books():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)

    with open(FILE, "r") as f:
        return json.load(f)


def save_books(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


@app.route("/", methods=["GET", "POST"])
def index():
    books = load_books()
    message = ""

    if request.method == "POST":
        new_book = {
            "id": len(books) + 1,
            "title": request.form["title"],
            "author": request.form["author"]
        }

        books.append(new_book)
        save_books(books)

        message = "Книга додана"

    return render_template("index.html", books=books, message=message)


@app.route("/book/<int:book_id>")
def book(book_id):
    books = load_books()

    for b in books:
        if b["id"] == book_id:
            return render_template("book.html", book=b)

    return "Book not found"

if __name__ == "__main__":
    app.run(debug=True)