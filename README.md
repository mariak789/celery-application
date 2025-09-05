# Celery Application

This project demonstrates a Python application using **Celery**, **FastAPI**, **PostgreSQL**, and **Redis**.  
It periodically fetches data from external APIs (or Faker for offline mode and due to random-data-api host instability) and stores it into the database.

---

##Features:
- **Periodic tasks with Celery Beat**
  - `fetch_users` – fetch users from API and store them in `users`
  - `fetch_addresses` – fetch addresses for users and store them in `addresses`
  - `fetch_credit_cards` – fetch credit cards for users and store them in `credit_cards`
- Data stored in PostgreSQL across 3 linked tables:
  - `users`
  - `addresses`
  - `credit_cards`
- **API Endpoints** (FastAPI):
  - `GET /health` – check service & DB availability
  - `GET /users` – list of users (id, ext_id, name, username, email)
  - `GET /users/{user_id}` – user details with addresses and credit cards

- **Repositories layer**: separates DB access from API routes
- **DTO / Pydantic response models**: typed and validated responses
- **Dockerized**: API, Celery worker, Celery beat, Redis, Postgres
- **Alembic** for database migrations
- **Pytest** with mocking for testing
- **Pre-commit hooks**: black, ruff, isort
- Deployable to **AWS EC2**

CREDIT CARD PROVIDER 

You can configure how credit card data is generated:
- CARDS_PROVIDER=remote -> fetch cards from Random Data API, cards saved in DB 
- CARDS_PROVIDER=faker -> generate cards locally using Faker, no external API dependency


## Stack

- **Python**: Celery, FastAPI, SQLAlchemy, Alembic, Pydantic
- **Database**: PostgreSQL
- **Broker**: Redis
- **Testing**: Pytest
- **Linting**: Black, Ruff, Isort
- **Containerization**: Docker + Docker Compose

---

## Getting started

### 1. Clone repository 

- ```git clone https://github.com/mariak789/celery-application.git```
- ```cd celery-application```

### 2. Configure environment 
Copy example env:

```cp .env.example .env``` 
(edit if needed, DB credentials, Redis URL)

### 3. Run with Docker 

```docker compose up --build``` 


## Celery tasks

The application defines 3 periodic tasks (scheduled via Celery Beat):
- `fetch_users`
- `fetch_addresses`
- `fetch_credit_cards`

Running tasks manually: 

### Fetch users 

``` docker compose exec worker celery -A app.celery_app.celery_app call fetch_users ```

### Fetch addresses

``` docker compose exec worker celery -A app.celery_app.celery_app call fetch_addresses ```

### Fetch credit cards 

``` docker compose exec worker celery -A app.celery_app.celery_app call fetch_credit_cards ```

### API Endpoints

### Health and database availability check

``` curl http://localhost:8000/health ```

### Users list 

``` curl http://localhost:8000/users ```

### User details

``` curl http://localhost:8000/users/1 ```

### Run tests

``` docker compose exec api pytest -v ```

### Linting 

``` pre-commit run --all-files ```
 
 ---

### Deployment of AWS 
- Create EC-2 instance (Amazon Linux 2023, t2.micro)
- Install Docker + Docker Compose 
- Clone repository & configure .env
- Run 

``` docker compose up -d ```

### Open in browser: 

Open http://56.228.24.150:8000/health 

