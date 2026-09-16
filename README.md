# Pharmacie Lite Backend

Backend for the Pharmacie Management System, built with [FastAPI](https://fastapi.tiangolo.com/).

## Requirements

- Python 3.9+
- Database (configured via environment variables)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd pharmacie-lite-backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory. This project requires configurations for:
   - Database connection
   - Authentication (JWT secrets, Hash pepper)
   
   *(Note: The `.env` file is excluded from version control for security).*

## Running the Application

To start the development server, you can run:

```bash
python main.py
```

Or using Uvicorn directly:

```bash
uvicorn main:app --reload
```

## API Documentation

Once the server is running, the interactive API documentation will be available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

- `app/` - Contains all modules like auth, system, and shared components.
- `main.py` - Entry point for the FastAPI application.
- `.env` - Environment variables configuration.
- `requirements.txt` - Project Python dependencies.
