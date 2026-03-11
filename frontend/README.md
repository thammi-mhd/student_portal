# Student Portal Frontend

A clean, responsive, and professional frontend for a **Face Recognition Attendance System**. Built with strictly HTML, CSS, and Vanilla JavaScript.

## Features
- **User Authentication**: Register and Login functionality using JWT tokens stored in `localStorage`.
- **Admin Dashboard**: Overview of system statistics (Total Students, Total Attendance records).
- **Student Management**: Register new students with face image capture and view the enrolled students directory.
- **Attendance System**: Upload or scan a face image to mark attendance. View historical attendance records.
- **Responsive Design**: Custom CSS Grid and Flexbox layout ensuring full compatibility with Mobile, Tablet, and Desktop screens.

## Project Structure
- `index.html` - Entry point containing auth redirection.
- `login.html` & `register.html` - Authentication views.
- `dashboard.html` - Main admin portal and statistics.
- `students.html` - Student registration and directory table.
- `attendance.html` - Image upload for face marking and records table.
- `css/style.css` - Global design system and layout.
- `js/api.js` - Global Fetch API methods with auth headers.
- `js/auth.js` - JWT token management and route protection.
- `js/dashboard.js`, `js/students.js`, `js/attendance.js` - Page-specific business logic.

## Local Execution
This is a standard static frontend. It can be served directly using any local web server or even Live Server in VS Code.

Using Python locally within the frontend folder:
```bash
python -m http.server 8000
```
Then open `http://localhost:8000/index.html` in your browser.

## Backend Integration
Ensure your Flask REST API is running. By default, the frontend expects `http://localhost:5000/api/v1`.
You can change the `API_BASE` variable inside `js/api.js` to point to your exact endpoints.
