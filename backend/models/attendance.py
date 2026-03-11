from datetime import datetime
from extensions import db

class Attendance(db.Model):
    __tablename__ = 'attendance_records'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    class_session_id = db.Column(db.Integer, db.ForeignKey('class_sessions.id'), nullable=True, index=True) # Optional for backward compatibility, required for new flow
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'class_session_id': self.class_session_id,
            'timestamp': self.timestamp.isoformat()
        }
