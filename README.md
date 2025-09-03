Celery Application

This project demonstrates a Python application using Celery, PostgreSQL, and Redis.
It periodically fetches data from external APIs and stores it into the database.

Features:
•	Periodic tasks with Celery Beat:
•   Fetch users and addresses from fakerapi.it
•   Fetch credit cards from Random Data Api (this source is frequently instable,    better to switch to Faker lib for offline work and stability)

Data stored in PostgreSQL accross 3 linked tables:
• users
• addresses
• credit_cards

Dockerized (API, Celery worker, Celery beat, Redis, Postgres)

• alembic for database migrations
• pytest with mocking for testing 
• Pre-commit hooks with black, ruff, isort
• Health check endpoint (/heath) as well as (/users), (/users/{user_id}) in the API 

Deployable to AWS (EC2)

Stack
	•	Python: Celery, FastAPI, SQLAlchemy, Alembic, Pydantic
	•	Database: PostgreSQL
	•	Broker: Redis
	•	Testing: Pytest
	•	Linting: Black, Ruff, Isort
	•	Containerization: Docker + Docker Compose


Getting started

1. Clone repository 

```git clone https://github.com/mariak789/celery-application.git```
```cd celery-application```

2. Configure environment 
Copy example env:

```cp .env.example .env``` 
(edit if needed, DB credentials, Redis URL)

3. Run with Docker 

```docker compose up --build``` 

Services started:
	•	api → http://localhost:8000
	•	db (Postgres) → localhost:5433
	•	redis → localhost:6379
	•	worker (Celery worker)
	•	beat (Celery scheduler)

4. Check health 

```curl http://localhost:8000/health```
# {"status": "ok"}

5. Run tasks manually 
Open worker container shell and call a task 

```docker compose exec worker celery -A app.celery_app.celery_app call fetch_users```

6. Database check 

```docker compose exec db psql -U postgres -d celery_app -c "\dt"```

7. Run tests
 
 at first, install dev-dependencies inside container
```docker compose exec api sh -lc "pip install -r requirements-dev.txt"```

 run tests
```docker compose exec api sh -lc "pytest -v"```

8. Linting 

```pre-commit run --all-files```


DEPLOYMENT on AWS 

	•	Create EC2 instance (Amazon Linux 2023 recommended)
	•	Install Docker + Docker Compose
	•	Clone repo + configure .env
	•	Run docker compose up -d
	•	Open http://56.228.24.150:8000/health 



