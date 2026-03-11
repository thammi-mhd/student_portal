# Face Recognition Attendance System Backend

A robust REST API backend powered by Flask, face_recognition, and SQLAlchemy to handle student attendance through facial recognition.

## Features
- **Authentication**: JWT-based login with role protection (admin/user).
- **Face Recognition**: Detects and extracts facial encodings securely.
- **Student Management**: Upload student details and face image via multipart data.
- **Attendance Marking**: Identifies student natively directly from uploaded temporary images.
- **Security**: Rate limiting via Flask-Limiter.
- **Docs**: Interactive API documentation powered by Swagger.
- **Logs**: Rotating file log mechanism for easy tracking of system behaviors.

## Installation

1. Clone the repository and navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Copy the example environment variables file and update it with your own settings:
   ```bash
   cp .env.example .env
   ```

## Running the Application

To start the backend server natively on your machine:
```bash
python app.py
```

The server will be available at `http://127.0.0.1:5000`.

## API Documentation

Interactive Swagger documentation is active automatically. Once the server is running, visit:
```
http://127.0.0.1:5000/api/docs
```

## Initial Setup Notes
- The database (SQLite) and necessary upload folders are created automatically on launch.
- The **first user** to register via `/api/v1/auth/register` is automatically granted the `admin` role. All subsequent registrations default to the standard user role.
