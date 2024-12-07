# Initial Setup

```
pip install poetry
poetry install
```

# To install new dependencies

```
poetry add <package-name>
```

# To Run the Application

```
docker compose up -d
poetry shell
uvicorn main:app --reload --port 8000
```

# Migrations

## To migrate to latest migration

```
poetry shell
alembic upgrade head
```

## To migrate downwards

```
poetry shell
alembic downgrade -1
```

## To generate new migration

```
poetry shell
alembic revision --autogenerate -m "migration message"
```

## To migrate to specific version

```
poetry shell
alembic upgrade <version>
```
