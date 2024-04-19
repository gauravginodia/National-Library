from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from library_application.models import db, User, UserRole, Book, Section, BookStatus, BookIssued
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import pytz
from .cache_instance import cache
from flask import flash
user_bp = Blueprint('user', __name__)


@user_bp.route('/api/signup', methods=['POST'])
def signup():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        user_role = UserRole(user_id=user.id, role_id=1)
        db.session.add(user_role)
        db.session.commit()

        return jsonify({"message": "User signed up successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/api/login', methods=['GET', 'POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token, "message": "User logged in successfully", "userName": user.name})
    else:
        return jsonify({"error": "Invalid email or password"}), 400


@user_bp.route('/api/track-last-login', methods=['POST'])
@jwt_required()
def track_last_login():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    user.last_logged = datetime.now(pytz.timezone('Asia/Kolkata'))
    db.session.commit()
    return jsonify({"message": "Last login date updated successfully"}), 200


@user_bp.route('/api/books', methods=['GET'])
@jwt_required()
def get_books():
    current_user_id = get_jwt_identity()
    user = UserRole.query.filter_by(user_id=current_user_id, role_id=1).first()
    if not user:
        return jsonify({'message': 'Unauthorized access!'}), 403

    books_data = []
    for book in Book.query.all():
        allocated = 0
        requested = 0
        read = 0

        # Check if the book is allocated to the current user
        allocation = BookStatus.query.filter_by(
            book_id=book.id, user_id=current_user_id, is_allocated=1).first()
        if allocation:
            allocated = 1

        # Check if the book is requested by the current user
        allocation = BookStatus.query.filter_by(
            book_id=book.id, user_id=current_user_id, is_requested=1).first()
        if allocation:
            requested = 1

        # Check if the current user has read the book
        user_book = BookIssued.query.filter_by(
            book_id=book.id, user_id=current_user_id, returned=1).first()
        if user_book:
            read = 1

        books_data.append({
            'id': book.id,
            'name': book.name,
            'authors': book.authors,
            'isbn': book.isbn,
            'section': book.section.name,
            'allocated': allocated,
            'requested': requested,
            'read': read,
            'rating': book.rating
        })

    return jsonify(books_data)


@user_bp.route('/api/request/book', methods=['POST'])
@jwt_required()
def request_book():
    current_user_id = get_jwt_identity()
    num_allocated_books = BookStatus.query.filter_by(
    user_id=current_user_id, is_allocated=1).count()
    num_requested_books = BookStatus.query.filter_by(
    user_id=current_user_id, is_requested=1).count()
    total_requested_books = num_allocated_books + num_requested_books

    if total_requested_books >= 5:
        return jsonify({'error': 'Only 5 books can be requested at a time'}), 400

    book_id = request.json.get('book_id')
    
    allocations = BookStatus.query.filter_by(
        book_id=book_id, user_id=current_user_id).first()
    print(allocations)
    if allocations:
        allocations.is_allocated = 0
        allocations.is_requested = 1
        allocations.date_of_issue = datetime.now(pytz.timezone('Asia/Kolkata'))
        allocations.return_date = datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=7)
        db.session.commit()
        return jsonify({'message': 'Book requested successfully'}), 200
    else:
        date_of_issue = datetime.now(pytz.timezone('Asia/Kolkata'))
        return_date = datetime.now(pytz.timezone(
            'Asia/Kolkata')) + timedelta(days=7)
        new_allocation = BookStatus(user_id=current_user_id, book_id=book_id, is_allocated=0,
                                    is_requested=1, date_of_issue=date_of_issue, return_date=return_date)
        print(new_allocation)
        db.session.add(new_allocation)
        db.session.commit()
        return jsonify({'message': 'Book requested successfully'}), 200
    


@user_bp.route('/api/return/book', methods=['POST'])
@jwt_required()
def return_book():
    current_user_id = get_jwt_identity()
    book_id = request.json.get('book_id')
    user_id = request.json.get('user_id')
    print(book_id)

    try:
        user_book = BookIssued.query.filter_by(
            book_id=book_id, user_id=user_id, returned=0).first()
        if user_book:
            user_book.returned = 1
            db.session.commit()
            allocation = BookStatus.query.filter_by(
            book_id=book_id, user_id=user_id, is_allocated=1).first()
            if allocation:
                allocation.is_allocated = 0
                allocation.is_requested = 0
                db.session.commit()
            return jsonify({"message": "Book returned successfully"}), 200
        else:
            return jsonify({"error": "User book record not found"}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred while returning the book: " + str(e)}), 500


@user_bp.route('/api/fetch_my_books', methods=['GET'])
@jwt_required()
def fetch_my_books():
    current_user_id = get_jwt_identity()
    user_role = UserRole.query.filter_by(user_id=current_user_id).first()
    if user_role and user_role.role_id == 1:
        issued_books = []
        try:

            user_books = BookIssued.query.filter_by(
                user_id=current_user_id, returned=0).all()
            for book in user_books:
                # For each BookIssued entry, access the related Book object to get details

                book_details = {
                    "book_id": book.book.id,
                    "user_id": book.user.id,
                    "name": book.book.name,
                    "isbn": book.book.isbn,
                    "authors": book.book.authors,
                    "date_of_issue": book.date_of_issue,
                    "return_date": book.return_date

                }
                issued_books.append(book_details)
            return jsonify(issued_books), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching allocated books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401


@user_bp.route('/api/fetch_returned_books', methods=['GET'])
@jwt_required()
def fetch_returned_books():
    current_user_id = get_jwt_identity()
    user_role = UserRole.query.filter_by(user_id=current_user_id).first()
    if user_role and user_role.role_id == 1:
        try:
            returned_books = BookIssued.query.filter_by(
                user_id=current_user_id, returned=1).all()

            returned_books_list = []
            for book in returned_books:
                print(book.user.id)
                returned_books_list.append({
                    'book_id': book.book.id,
                    'user_id': book.user.id,
                    'book_title': book.book.name,
                    'author': book.book.authors,
                    'section': book.book.section.name,
                    'feedback':book.feedback,
                    'rating':book.rating # Use alias to resolve ambiguity
                })

            return jsonify(returned_books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching returned books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401


@user_bp.route('/api/submit_feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    try:
        user_id = request.json.get('user_id')
        book_id = request.json.get('book_id')
        feedback = request.json.get('feedback')
        rating = request.json.get('rating')
        print(user_id)
        user_book = BookIssued.query.filter_by(
            user_id=user_id, book_id=book_id).first()
        if user_book:
            user_book.feedback = feedback
            user_book.rating = rating
            db.session.commit()

            # Calculate the average rating for the book
            average_rating = db.session.query(db.func.avg(BookIssued.rating)).filter(
                BookIssued.book_id == book_id).scalar()
            average_rating = round(average_rating)

            book = Book.query.get(book_id)
            if book:
                book.rating = average_rating
                db.session.commit()

            return jsonify({"message": "Feedback submitted successfully"}), 200
        else:
            return jsonify({"error": "User has not borrowed this book"}), 400
    except Exception as e:
        flash("Please borrow the book to submit Feedback","danger")

        return jsonify({"error": "An error occurred while submitting feedback: " + str(e)}), 500


@user_bp.route('/api/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book_details(book_id):
    current_user_id = get_jwt_identity()
    print(current_user_id)
    book = BookStatus.query.filter_by(
        book_id=book_id, user_id=current_user_id).first()
    is_allocated = book.is_allocated if book else 0
    is_requested = book.is_requested if book else 0
    button_text = ""
    if is_allocated:
        button_text = "Return"
    elif is_requested:
        button_text = "Requested"
    else:
        button_text = "Request"
    if not book:
        book=Book.query.filter_by(id=book_id).first()
        if book:
                return jsonify({
            'id': book.id,
            'name': book.name,
            'authors':book.authors,
            'content': book.content,
            'isbn': book.isbn,
            'rating':book.rating,
            'is_allocated':0,
            'is_requested': 0,
            'return_date': "Null",
            'user_id': current_user_id,
            'section_id': book.section_id,
            'button_text': "Request"
        })
        else:
            return jsonify({'error': 'Book not found'}), 404
    return jsonify({
        'id': book.book_id,
        'name': book.book.name,
        'authors': book.book.authors,
        'content': book.book.content,
        'isbn': book.book.isbn,
        'rating': book.book.rating,
        'is_allocated': book.is_allocated,
        'is_requested': book.is_requested,
        'return_date': book.return_date,
        'user_id': current_user_id,
        'section_id': book.book.section_id,
        'button_text': button_text
    })


@user_bp.route('/api/books/<int:book_id>/feedback', methods=['GET'])
@jwt_required()
def get_book_feedback(book_id):
    feedback = BookIssued.query.filter(BookIssued.book_id == book_id, BookIssued.feedback.isnot(None)).all()
    return jsonify([{
        'username': fb.user.name,
        'rating': fb.rating,
        'feedback': fb.feedback
    } for fb in feedback])


@user_bp.route('/api/sections/<int:section_id>/books', methods=['GET'])
@jwt_required()
def get_similar_books(section_id):
    try:
        current_user_id = get_jwt_identity()

        similar_books = Book.query.filter_by(section_id=section_id).all()
        print(similar_books)
        similar_books_data = []
        for book in similar_books:
            book_status = BookStatus.query.filter_by(
                book_id=book.id, user_id=current_user_id).first()
            is_allocated = book_status.is_allocated if book_status else 0
            is_requested = book_status.is_requested if book_status else 0

            button_text = ""
            if is_allocated:
                button_text = "Return"
            elif is_requested:
                button_text = "Requested"
            else:
                button_text = "Request"

            similar_books_data.append({
                'id': book.id,
                'name': book.name,
                'authors': book.authors,
                'isbn': book.isbn,
                'button_text': button_text
            })

        return jsonify(similar_books_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
