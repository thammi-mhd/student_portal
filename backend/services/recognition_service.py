import face_recognition
import numpy as np
from models.face_encoding import FaceEncoding
from extensions import db

class RecognitionService:
    @staticmethod
    def extract_encoding(image_path):
        """
        Loads an image, detects a face, and extracts its 128-dimensional encoding.
        Returns the encoding if exactly one face is detected, otherwise returns None.
        """
        try:
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 1:
                return face_encodings[0]
            elif len(face_encodings) > 1:
                return "Multiple faces detected"
            else:
                return "No face detected"
        except Exception as e:
            print(f"Error extracting encoding: {str(e)}")
            return None

    @staticmethod
    def extract_average_encoding(image_paths):
        """
        Takes a list of image paths, extracts encodings for each, 
        and averages them to create a robust face encoding.
        """
        valid_encodings = []
        for path in image_paths:
            encoding = RecognitionService.extract_encoding(path)
            # Only add if it's a valid numpy array (not an error string or None)
            if encoding is not None and not isinstance(encoding, str):
                valid_encodings.append(encoding)
                
        if not valid_encodings:
            return "No valid faces found in uploaded images"
            
        # Average all numpy arrays across axis 0
        average_encoding = np.mean(valid_encodings, axis=0)
        return average_encoding

    @staticmethod
    def identify_student(image_path, tolerance=0.5):
        """
        Loads an uploaded temporary image, extracts encoding, and compares it
        against all encodings stored in the database.
        Returns a tuple (student_id, message).
        """
        # Extract face encoding from the uploaded image
        encoding_result = RecognitionService.extract_encoding(image_path)
        
        if isinstance(encoding_result, str):
            # Error message string returned from extract_encoding
            return None, encoding_result
            
        if encoding_result is None:
            return None, "Error processing image"
            
        # Get all encodings from database
        stored_data = FaceEncoding.query.all()
        
        if not stored_data:
            return None, "No registered students found"
            
        # Separate encodings and student IDs
        known_encodings = [data.encoding for data in stored_data]
        student_ids = [data.student_id for data in stored_data]
        
        # Compare against all known encodings
        matches = face_recognition.compare_faces(known_encodings, encoding_result, tolerance=tolerance)
        face_distances = face_recognition.face_distance(known_encodings, encoding_result)
        
        # Find best match
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            student_id = student_ids[best_match_index]
            return student_id, "Match found"
        
        return None, "Student not recognized"
