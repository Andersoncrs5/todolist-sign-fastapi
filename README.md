# A Simple To-Do List with a Robust Login System

This project is a high-performance To-Do List API built with FastAPI. It's designed to showcase modern software development best practices, from secure user authentication to efficient data management.

## Key Features
**Secure JWT Authentication**: A robust login system uses JSON Web Tokens (JWT) to ensure all API routes are protected, granting access only to authenticated users.

**Comprehensive CRUD**: The application provides full CRUD (Create, Read, Update, Delete) functionality for both users and tasks, giving you complete control over your data.

**Advanced Data Handling**: Tasks can be efficiently queried, filtered, and paginated. The pagination and filtering features ensure optimal performance, even when managing large datasets.

**PostgreSQL Persistence**: The use of PostgreSQL as the database backend provides a secure, reliable, and scalable foundation for data storage.

**Quality Code Standards**: The project adheres to SOLID principles, resulting in clean, modular, and maintainable code. Pydantic is used for strict data validation, guaranteeing data integrity.

**Extensive Test Coverage**: Reliability is ensured through a comprehensive suite of unit and integration tests, validating that all features function as expected.

## Technologies Used
The project is built with the following libraries and tools:

**FastAPI**: A high-performance web framework for API development.

**Pydantic**: Used for data validation and serialization.

**SQLAlchemy with psycopg2**: The ORM for interacting with the PostgreSQL database.

**python-jose & passlib**: For JWT token management and password hashing.

**pytest & httpx**: For unit and integration testing.

**fastapi-filter & fastapi_pagination**: For advanced filtering and pagination.







