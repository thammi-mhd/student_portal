import os
from datetime import timedelta

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///attendance.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Uploads
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads"))
    STUDENT_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "students")
    TEMP_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "temp")
    
    # Validations
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_SIZE", 5 * 1024 * 1024)) # 5MB limit by default
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # Ensure upload folders exist
    @classmethod
    def init_app(cls):
        os.makedirs(cls.STUDENT_UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.TEMP_UPLOAD_FOLDER, exist_ok=True)
        
        # Also ensure logs directory exists
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
