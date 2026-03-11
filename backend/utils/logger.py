import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(app):
    """Setup application logging with rotating file handler"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    log_file = os.path.join(log_dir, "app.log")
    
    # Create logger
    logger = logging.getLogger('attendance_system')
    logger.setLevel(logging.INFO)
    
    # Format for logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler (10MB max size, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10485760, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Attach logger to app
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logging.INFO)
    
    app.logger.info("Application logging initialized")
    return logger
