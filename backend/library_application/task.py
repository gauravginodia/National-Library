import smtplib
from email.mime.text import MIMEText
from celery import shared_task
from datetime import datetime, timedelta
from library_application.models import BookIssued, db, BookStatus, User,Book,Section,UserRole
import pytz
from flask import render_template

@shared_task(ignore_result=False)
def return_overdue_books():
    current_time_ist = datetime.now(pytz.timezone('Asia/Kolkata'))
    print(current_time_ist)
    
    overdue_books = BookIssued.query.filter(
        BookIssued.return_date < current_time_ist,
        BookIssued.returned == 0
    ).all()
    print(overdue_books)
    
    for allocation in overdue_books:
        allocation.returned = 1  
        db.session.commit()
        book = BookStatus.query.filter_by(book_id=allocation.book_id, user_id=allocation.user_id, is_allocated=1).first()
        if book:
            book.is_allocated = 0
            book.is_requested = 0
            db.session.commit()

@shared_task(ignore_result=False)
def send_daily_reminder():
    yesterday = datetime.now(pytz.timezone('Asia/Kolkata')) - timedelta(days=1)
    users_to_remind = User.query.filter(User.last_logged < yesterday).all()
    for user in users_to_remind:
        send_email('Daily Reminder', user.email, 'Please visit our app!')

from sqlalchemy import func

@shared_task(ignore_result=False)
def send_monthly_report():
    users = UserRole.query.filter_by(role_id=1)

    for user_role in users:
        user = user_role.user
        
        books_issued_query = BookIssued.query.filter_by(user_id=user.id)
        books_issued_count = books_issued_query.count()
        
        sections_explored_query = Book.query.filter(BookIssued.user_id == user.id).distinct(Book.section_id)
        sections_explored_count = sections_explored_query.count()
        
        books_returned_query = BookIssued.query.filter_by(user_id=user.id, returned=1)
        books_returned_count = books_returned_query.count()
        
        average_rating = db.session.query(func.avg(BookIssued.rating)).filter(BookIssued.user_id == user.id).scalar()

        report_body = render_template(
            'monthly_report.html',
            user=user.name,
            books_issued=books_issued_count,
            sections_explored=sections_explored_count,
            books_returned=books_returned_count,
            average_rating=average_rating
        )

        send_monthly_email('Monthly Report', user.email, report_body)


def send_email(subject, recipient, body):
    sender_email = 'gauravginodiacollege@gmail.com'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())


def send_monthly_email(subject, recipient, body):
    sender_email = 'gauravginodiacollege@gmail.com'

    msg = MIMEText(body,"html")
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string().encode('utf-8'))
