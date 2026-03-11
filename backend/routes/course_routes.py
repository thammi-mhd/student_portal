from flask import Blueprint, jsonify
from extensions import db
from models.course import Course

course_bp = Blueprint('courses', __name__)

@course_bp.route('', methods=['GET'])
def get_courses():
    """
    Get all available courses.
    Publicly accessible or requires auth depending on needs, 
    but for now we just return the list.
    """
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200
