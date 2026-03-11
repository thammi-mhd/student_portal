from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.student import Student
from models.face_encoding import FaceEncoding
from services.face_service import FaceService
from services.recognition_service import RecognitionService
from utils.jwt_utils import admin_required
import os

student_bp = Blueprint('students', __name__)

@student_bp.route('/register', methods=['POST'])
@jwt_required()
@admin_required()
def register_student():
    """
    Register a new student and their face encoding (Admin Only)
    ---
    tags:
      - Students
    consumes:
      - multipart/form-data
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: roll_number
        in: formData
        type: string
        required: true
      - name: department
        in: formData
        type: string
        required: true
      - name: image
        in: formData
        type: file
        required: true
    responses:
      201:
        description: Student registered successfully
      400:
        description: Invalid input or missing data
    """
    # Validate form data (accepts 'images' list from new frontend or 'image' from old)
    files = request.files.getlist('images')
    if not files:
        if 'image' in request.files:
            files = [request.files['image']]
        else:
            return jsonify({"message": "No image data in the request"}), 400

    if not files or files[0].filename == '':
        return jsonify({"message": "No selected files"}), 400

    name = request.form.get('name')
    roll_number = request.form.get('roll_number')
    department = request.form.get('department')
    course_id = request.form.get('course_id') # New field

    if not name or not roll_number or not department:
        return jsonify({"message": "Missing required student details"}), 400
        
    if Student.query.filter_by(roll_number=roll_number).first():
        return jsonify({"message": "Student with this roll number already exists"}), 400

    # Process first image as the main profile picture
    main_image = files[0]
    image_path = FaceService.save_student_image(main_image, roll_number)
    
    if not image_path:
        return jsonify({"message": "Invalid file format for primary image."}), 400

    # Process remaining images (if any) for robust encoding
    temp_paths = []
    if len(files) > 1:
        temp_paths = FaceService.save_temp_images(files[1:])
        
    all_paths = [image_path] + temp_paths

    # Extract Encoding (Single or Average)
    if len(all_paths) > 1:
        encoding = RecognitionService.extract_average_encoding(all_paths)
    else:
        encoding = RecognitionService.extract_encoding(image_path)
        
    # Cleanup temp files immediately
    FaceService.delete_images(temp_paths)

    if isinstance(encoding, str): # Error strings
        FaceService.delete_image(image_path)
        return jsonify({"message": f"Face recognition failed: {encoding}"}), 400
    if encoding is None:
        FaceService.delete_image(image_path)
        return jsonify({"message": "Error processing face encodings"}), 500

    try:
        # Create student record (using course_id if provided)
        student = Student(
            name=name, 
            roll_number=roll_number, 
            department=department,
            course_id=course_id if course_id else None
        )
        db.session.add(student)
        db.session.commit()

        # Save face encoding
        face_encoding = FaceEncoding(
            student_id=student.id, 
            encoding=encoding, 
            image_path=os.path.basename(image_path)
        )
        db.session.add(face_encoding)
        db.session.commit()
        
        return jsonify({
            "message": "Student registered successfully",
            "student": student.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        FaceService.delete_image(image_path)
        return jsonify({"message": "Database error", "error": str(e)}), 500


@student_bp.route('', methods=['GET'])
@jwt_required()
@admin_required()
def get_students():
    """
    Get all registered students (Admin Only)
    ---
    tags:
      - Students
    responses:
      200:
        description: List of students
    """
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students]), 200


@student_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@admin_required()
def get_student(id):
    """
    Get a specific student by ID (Admin Only)
    ---
    tags:
      - Students
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Student details
      404:
        description: Student not found
    """
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict()), 200


@student_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_student(id):
    """
    Delete a student and their face data (Admin Only)
    ---
    tags:
      - Students
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Student deleted successfully
      404:
        description: Student not found
    """
    student = Student.query.get_or_404(id)
    
    # Delete image file if it exists
    if student.face_encoding:
        from config import Config
        image_path = os.path.join(Config.STUDENT_UPLOAD_FOLDER, student.face_encoding.image_path)
        FaceService.delete_image(image_path)
        
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": f"Student {id} deleted successfully"}), 200
