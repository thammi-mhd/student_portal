import os
from werkzeug.utils import secure_filename
from config import Config
from utils.validators import allowed_file

class FaceService:
    @staticmethod
    def save_student_image(file, roll_number):
        """
        Saves student image to the uploads/students folder.
        Uses roll_number for naming to ensure uniqueness.
        """
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"{roll_number}.{ext}")
            filepath = os.path.join(Config.STUDENT_UPLOAD_FOLDER, filename)
            file.save(filepath)
            return filepath
        return None

    @staticmethod
    def save_temp_image(file):
        """
        Saves temporary image for attendance matching.
        """
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.TEMP_UPLOAD_FOLDER, filename)
            file.save(filepath)
            return filepath
        return None

    @staticmethod
    def delete_image(filepath):
        """
        Deletes an image file if it exists.
        """
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
