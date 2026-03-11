document.addEventListener('DOMContentLoaded', () => {
    // Mobile Sidebar Toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (mobileToggle && sidebar) {
        mobileToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Fetch Dashboard Stats
    fetchDashboardData();
});

async function fetchDashboardData() {
    try {
        // Attempt to fetch students count
        const studentsResponse = await api.getStudents();
        // Depending on API structure, it could be an array or { data: [...] }
        let studentCount = 0;
        if (Array.isArray(studentsResponse)) {
            studentCount = studentsResponse.length;
        } else if (studentsResponse && studentsResponse.data) {
            studentCount = studentsResponse.data.length;
        } else if (studentsResponse && studentsResponse.students) {
            studentCount = studentsResponse.students.length;
        }
        document.getElementById('totalStudents').textContent = studentCount;

    } catch (error) {
        console.error("Dashboard error (Students):", error);
        document.getElementById('totalStudents').textContent = 'Error';
    }

    try {
        // Attempt to fetch attendance count
        const attendanceResponse = await api.getAttendance();
        let attendanceCount = 0;
        if (Array.isArray(attendanceResponse)) {
            attendanceCount = attendanceResponse.length;
        } else if (attendanceResponse && attendanceResponse.data) {
            attendanceCount = attendanceResponse.data.length;
        } else if (attendanceResponse && attendanceResponse.attendance) {
            attendanceCount = attendanceResponse.attendance.length;
        }
        document.getElementById('todayAttendance').textContent = attendanceCount;

    } catch (error) {
        console.error("Dashboard error (Attendance):", error);
        document.getElementById('todayAttendance').textContent = 'Error';
    }
}
