from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")

# Helper function to validate correct book_id
def validate_book(book_id):
    try:
        book = int(book_id)
    except:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))
    
    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message": f"book {book_id} not found"}, 404))

    return book


# To get a list of all books, and filter by title if desired
@books_bp.route("", methods=["GET"])
def read_all_books():

    #currently returns a correctly titled book, but not incorrect
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })

    return jsonify(books_response), 200


# To get one book, using helper function
@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)

    return jsonify(book.return_to_dict())


# To create a new book entry
@books_bp.route("", methods=["POST"])
def create_books():
    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"], 
        description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)



# To update a book
@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)
    
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({'error': f'Request must include title and decription.'}), 400

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book_id} successfully updated."))

# To delete a book
@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book # {book_id} successfully deleted."))



# Hello-World starter content
# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body

# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def say_hello_json():
#     return {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#         }

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body