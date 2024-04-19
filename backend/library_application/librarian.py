from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from library_application.models import db, User, UserRole, Section, Book, BookStatus, BookIssued
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import pytz
from dateutil import tz
from sqlalchemy import func

librarian_bp = Blueprint('librarian', __name__)

@librarian_bp.route('/api/librarian/login', methods=['POST'])

def login():
    
    email = request.json.get('email')
    password = request.json.get('password')
    
    user = User.query.filter_by(email=email, password=password).first()
   
    if user:
        librarian_user = UserRole.query.filter_by(user_id=user.id, role_id=2).first()  # Assuming 'librarian' role ID is 2
        if librarian_user:
            
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token, "message": "Librarian logged in successfully"})
        else:
            return jsonify({"error": "Invalid librarian credentials"}), 401
    else:
        return jsonify({"error": "Invalid email or password"}), 400

@librarian_bp.route('/api/add/new-section', methods=['POST'])
@jwt_required()
def add_section():
    
    name = request.json.get('name')
    date_created = request.json.get('date')
    description = request.json.get('description')
        
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first() 

    if user:
        try:
            date_created_utc = datetime.strptime(date_created, '%Y-%m-%d')  # Convert string to datetime object in UTC
            date_created_ist = date_created_utc.replace(tzinfo=tz.gettz('Asia/Kolkata'))
            print(date_created)
            section = Section(name=name, date_created=date_created_ist, description=description)
            db.session.add(section)
            db.session.commit()
            return jsonify({"message": "Section added successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while adding the section: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401


@librarian_bp.route('/api/sections', methods=['GET'])
@jwt_required()
def list_sections():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()  # Assuming 'librarian' role ID is 2

    if user:
        try:
            sections = Section.query.all()

            sections_list = []
            for section in sections:
                sections_list.append({
                    'id': section.id,
                    'name': section.name,
                    'date_created': section.date_created,
                    'description': section.description
                })

            return jsonify(sections_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching sections: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401

@librarian_bp.route('/api/add/book', methods=['POST'])
@jwt_required()
def addbook():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()

    if user:
        try:
            
            title = request.json.get('title')
            authorName = request.json.get('authorName')
            content = request.json.get('content')
            isbn=request.json.get('isbn')
            section_name = request.json.get('section') 
            print(section_name) # Updated to retrieve section ID
            rating = 0

            # Check if the section with provided ID exists
            section = Section.query.filter_by(name=section_name).first()
            print(section.id)
            if not section:
                return jsonify({"error": "Section does not exist"}), 404

            # Create and add the new book
            else:
                book = Book(name=title, content=content, authors=authorName,isbn=isbn,rating=rating, section_id=section.id)  # Associate with section
                db.session.add(book)
                db.session.commit()

            return jsonify({"message": "Book added successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while adding the book: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401
@librarian_bp.route('/api/books/allocate', methods=['POST'])
@jwt_required()
def grantbook():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()  # Assuming 'librarian' role ID is 1

    if user:
        try:
            
            book_id = request.json.get('book_id')
            user_id = request.json.get('user_id')

            # Get current time in IST
            current_time_ist = datetime.now(pytz.timezone('Asia/Kolkata'))

            # Check if the book allocation record exists
            books_allocation = BookStatus.query.filter_by(book_id=book_id, user_id=user_id, is_requested=1).first()

            if books_allocation:
                # Update allocation details
                books_allocation.is_allocated = 1
                books_allocation.is_requested = 0
                books_allocation.date_of_issue = current_time_ist
                books_allocation.return_date = current_time_ist + timedelta(days=7)
                db.session.commit()

                # Update or create user book record
                user_book = BookIssued.query.filter_by(user_id=user_id, book_id=book_id).first()
                if user_book:
                    user_book.date_of_issue = current_time_ist
                    user_book.return_date = current_time_ist + timedelta(days=7)
                    user_book.returned = 0
                else:
                    user_book = BookIssued(user_id=user_id, book_id=book_id, date_of_issue=current_time_ist, return_date=current_time_ist + timedelta(days=7), returned=0)
                    db.session.add(user_book)
                db.session.commit()

                return jsonify({"message": "Book allocated successfully"}), 200
            else:
                return jsonify({"error": "Book allocation record not found"}), 404

        except Exception as e:
            return jsonify({"error": "An error occurred while allocating the book: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401


@librarian_bp.route('/api/delete/request', methods=['DELETE'])
@jwt_required()
def reject_request():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()  # Assuming 'librarian' role ID is 1
    if user:
        try:
            allocation_id = request.json.get('allocation_id') 
            if allocation_id is None:
                return jsonify({"error": "Allocation ID is missing from request body"}), 400
            
            BookStatus.query.filter_by(id=allocation_id).delete()
            db.session.commit()
            return jsonify({"message": "Request deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while deleting the request: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401

@librarian_bp.route('/api/books/delete', methods=['DELETE'])
@jwt_required()
def deletebook():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()
    if user:
        try:
            
            book_id = request.json.get('book_id')
            if book_id is None:
                return jsonify({"error": "Book ID is missing from request body"}), 400
            
            # Query the book by its ID
            book = Book.query.get(book_id)
            if not book:
                return jsonify({"error": "Book not found"}), 404
            
            # Delete the book from the database
            db.session.delete(book)
            db.session.commit()

            return jsonify({"message": "Book deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while deleting the book: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401


@librarian_bp.route('/api/revoke/book', methods=['POST'])
@jwt_required()
def revokebook():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()
    
    allocation_id = request.json.get('allocation_id')
    book_id = request.json.get('book_id')
    user_id = request.json.get('user_id')

    if user:
        try:
            user_book = BookIssued.query.filter_by(book_id=book_id, user_id=user_id, returned=0).first()
            if user_book:
                user_book.returned = 1
                db.session.commit()
                books_allocation = BookStatus.query.filter_by(id=allocation_id).first()
                if books_allocation:
                    books_allocation.is_allocated = 0  # Mark the book as not allocated
                    books_allocation.is_requested = 0  # Reset request status
                    db.session.commit()
                else:
                    return jsonify({"error": "BookStatus record not found"}), 404
            else:
                return jsonify({"error": "User book record not found"}), 404
            return jsonify({"message": "Book returned successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while returning the book: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401


# Your Flask route to fetch librarian books
@librarian_bp.route('/api/fetch/librarian/books', methods=['GET'])
@jwt_required()
def list_books():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()

    if user:
        try:
            # Fetch all books from the database
            books = Book.query.all()

            # Construct list of books with additional information
            books_list = []
            for book in books:
                # Retrieve section name associated with the book
                section_name = Section.query.get(book.section_id).name if book.section_id else "N/A"

                # Determine availability status of the book
                availability = "Available"
                allocation = BookStatus.query.filter_by(book_id=book.id, is_allocated=1).first()
                if allocation:
                    availability = "Not Available"

                # Construct book data dictionary
                book_data = {
                    "book_id": book.id,
                    "book_name": book.name,
                    "authors": book.authors,
                    "isbn":book.isbn,
                    "section_name": section_name,
                    "availability": availability
                }
                books_list.append(book_data)

            # Return the books as JSON response
            return jsonify(books_list), 200

        except Exception as e:
            return jsonify({"error": "An error occurred while fetching books: " + str(e)}), 500

    else:
        return jsonify({"error": "Unauthorized access"}), 401


@librarian_bp.route('/api/librarian/allocated_books', methods=['PUT'])
@jwt_required()
def allocated_books():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()

    if user:
        try:
            allocated_books = BookStatus.query.filter_by(is_allocated=1).all()
            print(allocated_books)
            allocated_books_list = []
            for book in allocated_books:
                print(book.book.name)
                allocated_books_list.append({
                    'allocation_id': book.id,
                    'book_id': book.book_id,
                    'user_id': book.user_id,
                    'user_name': book.user.name, 
                    'book_name': book.book.name, 
                    'date_of_issue':book.date_of_issue,
                    'return_date':book.return_date
                    
                })
            print(allocated_books_list)

            return jsonify(allocated_books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching allocated books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401

@librarian_bp.route('/api/books/update', methods=['PUT'])
@jwt_required()
def updatebook(): 
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()
    if not user:
        return jsonify({"error": "Unauthorized access"}), 401
    try:
        
        book_id = request.json.get('book_id')
        book_name = request.json.get('book_name')
        author = request.json.get('author')
        isbn=request.json.get('isbn')

        # Query the book by its ID
        book = Book.query.get(book_id)
        print(book)
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Update the book details
        book.name = book_name
        book.authors = author
        book.isbn=isbn
        db.session.commit()

        return jsonify({"message": "Book updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update book: " + str(e)}), 500



@librarian_bp.route('/api/fetch/section/books', methods=['POST'])
@jwt_required()
def get_section_books():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()  # Assuming 'librarian' role ID is 2

    if user:
        try:
            
            section_id = request.json.get('section_id')

            if section_id is None:
                return jsonify({"error": "Section ID is required"}), 400

            # Query books based on the section_id
            books = Book.query.filter_by(section_id=section_id).all()

            # Construct list of books
            books_list = []
            for book in books:
                books_list.append({
                    'book_id': book.id,
                    'book_name': book.name,
                    'author': book.authors,
                    'isbn':book.isbn,
                    'rating': book.rating
                    # Add other fields as needed
                })

            return jsonify(books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching section books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401



@librarian_bp.route('/api/delete/section/<int:section_id>', methods=['DELETE'])
@jwt_required()
def delete_section(section_id):
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()

    if user:
        try:
            # Fetch the section by its ID
            section = Section.query.get(section_id)
            if not section:
                return jsonify({"error": "Section not found"}), 404
            
            # Delete the section
            db.session.delete(section)
            db.session.commit()

            return jsonify({"message": "Section and associated books deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while deleting the section: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401

@librarian_bp.route('/api/books/requested', methods=['GET'])
@jwt_required()
def requested_books():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=2).first()  
    if user:
        try:
            requested_books = BookStatus.query \
                .join(Book, BookStatus.book_id == Book.id) \
                .join(Section, Book.section_id == Section.id) \
                .join(User, BookStatus.user_id == User.id) \
                .add_columns(
                    BookStatus.id.label('allocation_id'),
                    Book.id.label('book_id'),
                    Book.name.label('book_name'),
                    Section.id.label('section_id'),
                    Section.name.label('section_name'),
                    User.id.label('user_id'),
                    User.name.label('user_name')
                ) \
                .filter(BookStatus.is_requested == 1).all()

            requested_books_list = []
            for book in requested_books:
                requested_books_list.append({
                    'allocation_id': book.allocation_id,
                    'book_id': book.book_id,
                    'book_name': book.book_name,
                    'section_id': book.section_id,
                    'section_name': book.section_name,
                    'user_id': book.user_id,
                    'user_name': book.user_name
                })
            print(requested_books_list)
            return jsonify(requested_books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching requested books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401



@librarian_bp.route('/api/section/books/distribution' ,methods=['GET'])
@jwt_required()
def get_section_books_distribution():
    print("inside get section")
    section_books_count = db.session.query(Section.name, db.func.count(Book.id)).join(Book).group_by(Section.name).all()
    labels = [result[0] for result in section_books_count]
    data = [result[1] for result in section_books_count]
    print(labels,data)
    return jsonify({"labels": labels, "data": data})

@librarian_bp.route('/api/book/issuances/trend',methods=['GET'])
@jwt_required()
def get_book_issuances_trend():
    print("inside get book")
    issuances_by_date = db.session.query(db.func.date(BookIssued.date_of_issue), db.func.count(BookIssued.id)).group_by(db.func.date(BookIssued.date_of_issue)).all()
    labels = [result[0] for result in issuances_by_date]
    data = [result[1] for result in issuances_by_date]
    print(labels,data)
    return jsonify({"labels": labels, "data": data})



@librarian_bp.route('/api/section/books/issued', methods=['GET'])
@jwt_required()
def get_section_books_issued():
    print("books per section issued:")
    section_books_issued = db.session.query(Section.name, func.count(BookIssued.id)) \
                                     .join(Book, Section.books) \
                                     .join(BookIssued) \
                                     .group_by(Section.name) \
                                     .all()
    labels = [result[0] for result in section_books_issued]
    data = [result[1] for result in section_books_issued]   
    print(labels,data)
    return jsonify({"labels": labels, "data": data})

@librarian_bp.route('/api/books/ratings', methods=['GET'])
@jwt_required()
def get_books_by_ratings():
    print("inside get books by ratings")
    books_by_ratings = Book.query.with_entities(Book.name,Book.rating).all()
    ratings = [result[0] for result in books_by_ratings]
    counts = [result[1] for result in books_by_ratings]
    print(ratings, counts)
    return jsonify({"labels": ratings, "data": counts})

