
from dotenv import load_dotenv
from library_application import create_app
from library_application.worker import celery_init_app


load_dotenv()

app = create_app()
celery_app=celery_init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
