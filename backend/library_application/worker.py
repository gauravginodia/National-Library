from celery import Celery, Task
from celery.schedules import crontab
from library_application.task import return_overdue_books  # Assuming your task is defined in tasks.py

def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)

    # Define Celery configuration here
    celery_config = {
        "broker_url": "redis://localhost:6379/1",
        "result_backend": "redis://localhost:6379/2",
        "broker_connection_retry_on_startup": True,
        "timezone": "Asia/Kolkata"
    }   

    celery_app.conf.update(celery_config)
    
    
   # Define Celery beat schedule
    celery_app.conf.beat_schedule = {
        'check_overdue_books': {
            'task': 'library_application.task.return_overdue_books',
            'schedule': crontab(),  
        },
        'check_last_visit':{
            'task':'library_application.task.send_daily_reminder',
            'schedule':crontab(hour=16,minute=0),
            
        },
     
 
   'monthly_report':{
            'task':'library_application.task.send_monthly_report',
            'schedule':crontab(day_of_month='1', hour='0', minute='0'),
            
        }
    }
    return celery_app