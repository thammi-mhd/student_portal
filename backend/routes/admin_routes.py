from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.user import User
from models.attendance import Attendance
from utils.jwt_utils import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required()
def get_users():
    """
    Get all registered users (Admin Only)
    ---
    tags:
      - Admin
    responses:
      200:
        description: List of users
    """
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@admin_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_user(id):
    """
    Delete a user by ID (Admin Only)
    ---
    tags:
      - Admin
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
    """
    user = User.query.get_or_404(id)
    
    # Prevent admin from deleting themselves if needed,
    # but for now we just delete
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {id} deleted successfully"}), 200

@admin_bp.route('/attendance', methods=['GET'])
@jwt_required()
@admin_required()
def get_attendance_records():
    """
    Get all attendance records (Admin Only)
    ---
    tags:
      - Admin
    responses:
      200:
        description: List of all attendance records
    """
    records = Attendance.query.order_by(Attendance.timestamp.desc()).all()
    # We could also join with Student to return student names here
    from models.student import Student
    
    result = []
    for record in records:
        student = Student.query.get(record.student_id)
        record_dict = record.to_dict()
        record_dict['student_name'] = student.name if student else 'Unknown'
        record_dict['roll_number'] = student.roll_number if student else 'Unknown'
        result.append(record_dict)
        
    return jsonify(result), 200
