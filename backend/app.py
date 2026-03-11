import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import load_dotenv
from flask_cors import CORS

from config import Config
from utils.logger import setup_logger
from utils.limiter import init_limiter
from extensions import db, jwt

# Load environment variables
load_dotenv()

# Initialize extensions
swagger = Swagger()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend requests
    CORS(app)

    # Initialize folders and logs
    Config.init_app()
    setup_logger(app)

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    init_limiter(app)
    
    # Swagger config
    swagger.init_app(app)

    # Register blueprints (routes)
    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    from routes.attendance_routes import attendance_bp
    from routes.admin_routes import admin_bp
    from routes.course_routes import course_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(student_bp, url_prefix='/api/v1/students')
    app.register_blueprint(attendance_bp, url_prefix='/api/v1/attendance')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(course_bp, url_prefix='/api/v1/courses')

    # Global error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"message": "Bad request", "error": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"message": "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"message": "Forbidden"}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(429)
    def ratelimit_handler(error):
        return jsonify({"message": "Rate limit exceeded", "error": str(error)}), 429

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"message": "Internal server error"}), 500

    # Ensure tables are created
    with app.app_context():
        import models  # Import models so SQLAlchemy creates tables
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    # Run the server
    app.run(host='0.0.0.0', port=5000, debug=True)
