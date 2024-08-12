postgres_creds = {
    "user": "postgres",
    "host": "localhost",
    "db": "book_management_in",
    "password": ""
}
creds = {
    "username": "admin",
    "password": "password"
}
DATABASE_URL = f'postgresql+asyncpg://{postgres_creds["user"]}:{postgres_creds["password"]}@{postgres_creds["host"]}/{postgres_creds["db"]}'
