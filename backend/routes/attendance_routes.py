from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.attendance import Attendance
from models.student import Student
from services.face_service import FaceService
from services.recognition_service import RecognitionService
from utils.limiter import limiter

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/mark', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def mark_attendance():
    """
    Mark student attendance via face recognition
    ---
    tags:
      - Attendance
    consumes:
      - multipart/form-data
    parameters:
      - name: image
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Attendance marked successfully
      400:
        description: Face not recognized or processing error
      404:
        description: Student not found
    """
    if 'image' not in request.files:
        return jsonify({"message": "No image part in the request"}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Save temporary image for recognition
    temp_path = FaceService.save_temp_image(file)
    if not temp_path:
        return jsonify({"message": "Invalid file format. Allowed: png, jpg, jpeg"}), 400

    try:
        # Match face against database
        student_id, message = RecognitionService.identify_student(temp_path, tolerance=0.5)

        if student_id:
            # Check if student exists
            student = Student.query.get(student_id)
            if not student:
                return jsonify({"message": "Student record not found"}), 404

            if not student.course_id:
                return jsonify({"message": "Student is not enrolled in any course"}), 400

            # Find active class session for student's course
            from datetime import datetime
            now = datetime.utcnow()
            current_date = now.date()
            current_time = now.time()

            from models.class_session import ClassSession
            active_session = ClassSession.query.filter(
                ClassSession.course_id == student.course_id,
                ClassSession.date == current_date,
                ClassSession.start_time <= current_time,
                ClassSession.end_time >= current_time
            ).first()

            if not active_session:
                return jsonify({"message": "No active class session found for your course right now."}), 400

            # Check if attendance is already recorded for this session
            existing_attendance = Attendance.query.filter_by(
                student_id=student.id,
                class_session_id=active_session.id
            ).first()

            if existing_attendance:
                return jsonify({"message": "Attendance already marked for this session."}), 400

            # Mark attendance
            attendance_record = Attendance(
                student_id=student_id,
                class_session_id=active_session.id,
                timestamp=now
            )
            db.session.add(attendance_record)
            db.session.commit()

            response = {
                "message": "Attendance marked successfully",
                "session": {"subject": active_session.subject, "id": active_session.id},
                "student": student.to_dict(),
                "timestamp": attendance_record.timestamp.isoformat()
            }
            status_code = 200
        else:
            response = {"message": message}
            status_code = 400
            
    except Exception as e:
        response = {"message": "Error marking attendance", "error": str(e)}
        status_code = 500
        
    finally:
        # Clean up temporary image
        FaceService.delete_image(temp_path)

    return jsonify(response), status_code
