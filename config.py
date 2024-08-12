import os

postgres_creds = {
    "user": "postgres",
    "host": "localhost",
    "db": "book_management",
    "password": "postgres"
}
creds = {
    "username": "admin",
    "password": "password"
}
DATABASE_URL = os.getenv("DATABASE_URL", f'postgresql+asyncpg://{postgres_creds["user"]}:{postgres_creds["password"]}@{postgres_creds["host"]}/{postgres_creds["db"]}')
