# Library Management Website

## Description
This project is a library management website built with Flask for the API backend and Vue.js for the user interface. Vue.js is utilized with the CLI for advanced development capabilities, while Bootstrap provides styling. The database is managed with SQLite, and Redis is employed for caching. Additionally, Redis and Celery are used for batch jobs.

## Demo Video

<iframe width="560" height="315" src="https://www.youtube.com/watch?v=F7sSOhsArE4" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Features
- Flask backend for API endpoints.
- Vue.js frontend with advanced CLI features.
- Bootstrap for responsive and sleek UI design.
- SQLite for database management.
- Redis for caching frequently accessed data.
- Redis and Celery for batch job processing.

## Prerequisites
Before running this project locally, ensure you have the following installed:
- Node.js and npm (for Vue.js)
- Python (for Flask)
- Redis server
- Celery (Python library)
- SQLite (usually included with Python installations)

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/gauravginodia/National-Library
   ```

2. Install frontend dependencies:
   ```
   cd frontend_library
   npm install
   ```

3. Install backend dependencies (recommended to use a virtual environment):
   ```
   cd ../backend
   pip install -r requirements.txt
   ```

4. Start Redis server:
   ```
   redis-server
   ```

## Usage
1. Start the Celery worker & beat:
   ```
   cd backend
   celery -A app.celery_app worker --l INFO
   celery -A app.celery_app beat --l INFO
   ```

2. Start the Flask backend:
   ```
   cd backend
   python app.py
   ```

3. Start the Vue.js frontend:
   ```
   cd ../frontend_library
   npm run serve
   ```

4. Access the application in your browser at `http://localhost:8080`.


## Acknowledgements
- Flask: https://flask.palletsprojects.com/
- Vue.js: https://vuejs.org/
- Bootstrap: https://getbootstrap.com/
- SQLite: https://www.sqlite.org/
- Redis: https://redis.io/
- Celery: https://docs.celeryproject.org/

## Contact
For any inquiries or support, please contact gauravginodia02@gmail.com.
