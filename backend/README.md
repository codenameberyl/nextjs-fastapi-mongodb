# FastAPI + MongoDB Starter Template

This is a starter template for building FastAPI applications with MongoDB as the database. The template includes modular code for database connections and JWT-based authentication, scalable, and easy to extend.

## Folder Structure

```plaintext
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py
│   ├── config.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│       ├── __init__.py
│       ├── auth.py
└── frontend/
```

## Features

- **MongoDB Connection**: Asynchronous connection to MongoDB using Motor.
- **JWT Authentication**: Token-based authentication with expiration handling.
- **Dependency Injection**: Reusable functions for database access and authentication.

---

## Prerequisites

- Python 3.9+
- MongoDB (local or hosted, e.g., MongoDB Atlas)
- [pip](https://pip.pypa.io/en/stable/)

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/codenameberyl/nextjs-fastapi-mongodb.git
cd nextjs-fastapi-mongodb/backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory and configure the following variables:

```env
PROJECT_NAME=yourprojectname # Replace with your project name
API_V1_STR=yourapiversionstring # Replace with your api version string
DATABASE_URL=mongodb://localhost:27017  # Replace with your MongoDB connection string
DATABASE_NAME=yourdatabaname # Replace with your database name
SECRET_KEY=supersecretkey  # Replace with a strong secret key (openssl rand -base64 32 or openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Start the Server

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

---

## API Endpoints

### Base URL: `http://127.0.0.1:8000`

### Authentication Endpoints (`/api/v1/auth`)

1. **Register User**
   - **POST** `/register`
   - Request Body:
     ```json
     {
       "username": "user1",
       "email": "user1@example.com",
       "password": "securepassword"
       "confirm_password": "securepassword"
     }
     ```
   - Response:
     ```json
     {
       "id": "63e1f4b66c2a5e50b4a3bcd7",
       "username": "user1",
       "email": "user1@example.com"
     }
     ```

2. **Login**
   - **POST** `/login`
   - Request Body:
     ```json
     {
       "username": "user1",
       "password": "securepassword"
     }
     ```
   - Response:
     ```json
     {
       "access_token": "jwt_token",
       "token_type": "bearer"
     }
     ```

---

## Environment Variables

### Required Variables

| Variable                      | Description                                    | Example                            |
|-------------------------------|------------------------------------------------|------------------------------------|
| `PROJECT_NAME`                | Your project name                              | `FastAPI Project`        |
| `API_V1_STR`                  | Your API version string                        | `/api/v1`        |
| `DATABASE_URL`                | MongoDB connection string                      | `mongodb://localhost:27017`        |
| `DATABASE_NAME`               | MongoDB database name                          | `yourdatabasename`        |
| `SECRET_KEY`                  | Secret key for JWT token signing               | `supersecretkey`                   |
| `ALGORITHM`                   | JWT token signing algorithm                    | `HS256`                            |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes               | `30`                               |

### Example `.env` File

```env
PROJECT_NAME=yourprojectname
API_V1_STR=yourapiversionstring
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=yourdatabaname
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## MongoDB Setup

### Connecting to MongoDB
The `connect_to_mongo` function establishes an asynchronous connection to the MongoDB database using the `AsyncIOMotorClient` from Motor.

- **Function**:
  ```python
  async def connect_to_mongo():
      global motor_client
      motor_client = AsyncIOMotorClient(settings.DATABASE_URL)
  ```

- **Usage**:
  This function is typically called during application startup.

### Closing MongoDB Connection
The `close_mongo_connection` function ensures that the database connection is properly closed when the application shuts down.

- **Function**:
  ```python
  async def close_mongo_connection():
      global motor_client
      if motor_client:
          motor_client.close()
  ```

### Accessing the Database
The `get_database` function provides access to the database instance.

- **Function**:
  ```python
  async def get_database():
      return motor_client[settings.DATABASE_NAME]
  ```

---

## JWT Authentication

### JWT Decoding
The `get_current_user` function validates and decodes a JWT token provided in the `Authorization` header. If the token is invalid or expired, it raises an `HTTPException`.

- **Function**:
  ```python
  async def get_current_user(
      credentials: HTTPAuthorizationCredentials = Security(security),
  ):
      try:
          payload = jwt.decode(
              credentials.credentials,
              settings.SECRET_KEY,
              algorithms=[settings.ALGORITHM],
          )
          if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
              raise HTTPException(status_code=401, detail="Token expired")
          return payload
      except jwt.InvalidTokenError:
          raise HTTPException(status_code=401, detail="Invalid token")
  ```

- **Key Features**:
  - Decodes the JWT using the secret key and algorithm defined in `.env`.
  - Checks for token expiration.
  - Returns the decoded payload if the token is valid.

### JWT Security
The `HTTPBearer` class is used to enforce token-based authentication. It automatically extracts the token from the `Authorization` header.

- **Token Format**:
  ```http
  Authorization: Bearer <token>
  ```

---

## Project Structure

- **`app/main.py`**: Entry point of the application.
- **`app/api/v1/endpoints/auth.py`**: Contains authentication endpoints.
- **`app/models/user.py`**: User model for MongoDB.
- **`app/schemas/user.py`**: Pydantic schemas for user-related data validation.
- **`app/services/auth.py`**: Helper functions for authentication (e.g., password hashing, token generation).
- **`app/config.py`**: Centralized configuration using environment variables.
- **`app/dependencies.py`**: Shared dependencies like database connections.

---

## Development Tips

1. **Use a Debugger**:
   - Run the app in debug mode using `uvicorn app.main:app --reload`.

2. **Test API with Swagger**:
   - FastAPI automatically generates Swagger documentation.
   - Access it at `http://127.0.0.1:8000/docs`.

3. **MongoDB Connection**:
   - Ensure MongoDB is running locally or replace `DATABASE_URL` with your MongoDB Atlas URI.

---

## Deployment

1. **Use a Production WSGI Server**:
   - Deploy with a production server like Gunicorn or Uvicorn.
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Configure `.env` Variables**:
   - Ensure your `.env` file is not included in your repository. Use a secrets manager or environment variables for production.

3. **Containerization (Optional)**:
   - Use Docker to containerize your application for easy deployment.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## Contact

For questions or support, reach out to:

- **Email**: abiolaonasanya22@gmail.com
- **GitHub**: [codenameberyl](https://github.com/codenameberyl)

---
