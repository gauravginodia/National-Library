from flask import Blueprint,Flask ,request, jsonify
from flask_mail import Mail
from library_application.models import db,User,UserRole,BookIssued,BookStatus,Book,Section,Role
from library_application.user import user_bp
from library_application.librarian import librarian_bp
import requests
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from datetime import datetime, timedelta
import os
from .cache_instance import cache

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
    app.config['JWT_SECRET_KEY'] = 'Cd73qJfFoV4etl7yDrwd4EShDAzhXvlX' 
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(app)
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465  # SSL Port
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'gauravginodiacollege@gmail.com'
      
 

    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST']='localhost'
    app.config['CACHE_REDIS_PORT']=6379
    app.config['CACHE_DEFAULT_TIMEOUT']=300
    cache.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(librarian_bp)

    with app.app_context():
        db.create_all()
        fill_database()


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/bookcover', methods=['GET', 'POST'])
    def get_book_cover():
        book_title = request.args.get('book_title')
        author_name = request.args.get('author_name')
        isbn = request.args.get('isbn')
        cache_key = f'book_cover_{isbn}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data)
        api_url = f'https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg'
        print(api_url)
        try:
            cache.set(cache_key, api_url, timeout=600)
            return jsonify(api_url)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app

def fill_database():
    if db.session.query(User).count() == 0:
        librarian = User(name='Librarian', email='librarian@gmail.com', password='123')
        user = User(name='User', email='gauravginodia02@gmail.com', password='iit')
        db.session.add(librarian)
        db.session.add(user)

    if db.session.query(Role).count() == 0:
        role1 = Role(role_name='User')
        role2 = Role(role_name='Librarian')
        db.session.add(role1)
        db.session.add(role2)

    if db.session.query(UserRole).count() == 0:
        user_role = UserRole(user_id=2, role_id=1)
        librarian_role = UserRole(user_id=1, role_id=2)
        db.session.add(user_role)
        db.session.add(librarian_role)

    if db.session.query(Section).count() == 0:
        section1 = Section(name='Fiction', description='Books of fictional genres')
        section2 = Section(name='Non-fiction', description='Books of non-fictional genres')
        db.session.add(section1)
        db.session.add(section2)

    if db.session.query(Book).count() == 0:
        book1 = Book(name='God of Small Things', content='', authors='Arundhati Roy', isbn='9788186939024',section_id=1)
        db.session.add(book1)
       

    db.session.commit()
