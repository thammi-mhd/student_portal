Face Recognizer
Overview

Face Recognizer is a Python-based computer vision project that detects and recognizes human faces using machine learning techniques. The system captures facial images, encodes facial features, and compares them with stored data to identify individuals.

This project demonstrates how face recognition can be used for applications such as automated attendance systems, identity verification, and security systems.

Features

Real-time face detection using a webcam

Face recognition using encoded facial features

Dataset creation for storing face images

Automatic attendance marking

CSV-based attendance storage

Simple and modular Python project structure

Technologies Used

Python

OpenCV

NumPy

Face Recognition Library

CSV for attendance storage

Face recognition systems typically work by detecting a face, extracting unique facial features, and comparing them with previously stored encodings to identify the person.

Project Structure
face_recognizer/
│
├── dataset/
│ └── images of registered students
│
├── encodings/
│ └── stored facial encodings
│
├── attendance/
│ └── attendance.csv
│
├── capture_images.py
├── train_model.py
├── recognize_faces.py
├── requirements.txt
└── README.md
Installation

Clone the repository

git clone https://github.com/thammi-mhd/face_recognizer.git
cd face_recognizer

Create a virtual environment

python -m venv venv

Activate the virtual environment

Windows

venv\Scripts\activate

Linux or macOS

source venv/bin/activate

Install dependencies

pip install -r requirements.txt
Usage

1. Capture Face Images

Run the image capture script to create a dataset of faces.

python capture_images.py

This will collect multiple images of each person and store them in the dataset directory.

2. Train the Model
   python train_model.py

This step generates face encodings from the dataset and saves them for recognition.

3. Start Face Recognition
   python recognize_faces.py

The webcam will start and the system will identify faces based on the trained dataset.

4. Attendance Recording

When a face is recognized, the system records the person's name and timestamp in a CSV file.

Example:

Name,Time
John,09:01:23
Alex,09:03:11
Requirements

Example dependencies:

opencv-python
face-recognition
numpy
pandas
Applications

Automated attendance systems

Access control systems

Smart surveillance systems

Identity verification systems

Future Improvements

GUI interface for easier usage

Database integration instead of CSV

Support for multiple cameras

Deployment as a web application

Improved model accuracy with larger datasets

Author

Mahammad Thameez

GitHub: https://github.com/thammi-mhd
