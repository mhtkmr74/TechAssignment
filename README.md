# Book Management System in Python

## Description
This is a Book Management System implemented in Python using the Quart web framework and SQLAlchemy for asynchronous database interactions. The system allows you to manage books and their reviews through RESTful APIs, with endpoints to create, retrieve, update, and delete both books and reviews.

## Prerequisites
Before running the application, ensure that the following prerequisites are met:

- Python 3.8+ installed on your system
- PostgreSQL database configured and running
- Necessary permissions to create and manage a database

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/mhtkmr74/TechAssignment
   ```

## Install Requirements:
    ```
    python -m pip install -r requirements.txt
    ```

## Update config.py:

Modify the config.py file with your PostgreSQL credentials and user authentication details. These credentials will be used to authenticate all REST API calls.

# Default credentials:
Username: admin
Password: password

## Create the Database:

The application will automatically migrate the required tables, but you'll need to create the database manually if it doesn't already exist. This step may require additional permissions.

## Running the Application
To start the Quart server, run the following command:

```
hypercorn app:app --bind 127.0.0.1:8000
```

Once the server is running, you can access the Swagger UI to interact with the API:

## Swagger UI: http://127.0.0.1:8000/api/doc

## Running Tests
To run the test suite, navigate to the tests/ directory and execute the following command:
```
cd tests/
pytest
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.