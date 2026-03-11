document.addEventListener('DOMContentLoaded', () => {
    // Mobile Sidebar Toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (mobileToggle && sidebar) {
        mobileToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Handle File Input Preview
    const fileInput = document.getElementById('faceImage');
    const imgPreview = document.getElementById('imagePreview');
    const uploadText = document.getElementById('uploadText');

    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            uploadText.textContent = `Selected: ${file.name}`;
            const reader = new FileReader();
            reader.onload = function(e) {
                imgPreview.src = e.target.result;
                imgPreview.style.display = 'block';
            }
            reader.readAsDataURL(file);
        } else {
            uploadText.textContent = 'Click or drag an image here to upload for face training.';
            imgPreview.style.display = 'none';
            imgPreview.src = '';
        }
    });

    // Handle Form Submission
    const addStudentForm = document.getElementById('addStudentForm');
    addStudentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('addStudentBtn');
        btn.textContent = 'Registering...';
        btn.disabled = true;

        const formData = new FormData();
        formData.append('name', document.getElementById('studentName').value);
        formData.append('roll_number', document.getElementById('rollNumber').value);
        formData.append('department', document.getElementById('department').value);
        
        // Append image (key typically expected as 'image' or 'file', fallback to generic)
        const file = document.getElementById('faceImage').files[0];
        if(file) {
            formData.append('image', file);
            formData.append('file', file);
        }

        try {
            await api.createStudent(formData);
            showAlert('studentAlert', 'Student registered successfully', 'success');
            addStudentForm.reset();
            imgPreview.style.display = 'none';
            uploadText.textContent = 'Click or drag an image here to upload for face training.';
            fetchStudents(); // Refresh table
        } catch (error) {
            showAlert('studentAlert', error.message || 'Failed to register student.', 'error');
        } finally {
            btn.textContent = 'Register Student';
            btn.disabled = false;
        }
    });

    // Load Initial Data
    fetchStudents();
});

async function fetchStudents() {
    const tbody = document.getElementById('studentsTableBody');
    tbody.innerHTML = '<tr><td colspan="5" class="text-center">Loading students...</td></tr>';
    
    try {
        const response = await api.getStudents();
        let students = [];
        
        if (Array.isArray(response)) {
            students = response;
        } else if (response && response.data) {
            students = response.data;
        } else if (response && response.students) {
            students = response.students;
        }

        if (students.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center" style="color: var(--text-muted);">No students found. Register one above.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        students.forEach(student => {
            const tr = document.createElement('tr');
            
            // Handle various likely JSON object structures from a Python backend
            const id = student.id || student._id || student.student_id || 'N/A';
            const name = student.name || 'N/A';
            const rollNumber = student.roll_number || student.rollNumber || student.roll_no || 'N/A';
            const dept = student.department || student.dept || 'N/A';

            tr.innerHTML = `
                <td>${id}</td>
                <td style="font-weight: 500;">${name}</td>
                <td>${rollNumber}</td>
                <td><span style="background-color: #eff6ff; color: var(--primary); padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">${dept}</span></td>
                <td>
                    <button class="btn btn-danger" style="padding: 0.25rem 0.75rem; font-size: 0.75rem; width: auto;" onclick="deleteStudent('${id}')">Delete</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Fetch students error:", error);
        tbody.innerHTML = `<tr><td colspan="5" class="text-center" style="color: var(--danger);">Failed to load students. ${error.message}</td></tr>`;
    }
}

// Attach function to window so it can be called from onclick attribute
window.deleteStudent = async function(id) {
    if (!confirm('Are you sure you want to delete this student?')) return;
    
    try {
        await api.deleteStudent(id);
        showAlert('studentAlert', 'Student deleted successfully', 'success');
        fetchStudents();
    } catch (error) {
        showAlert('studentAlert', error.message || 'Failed to delete student.', 'error');
    }
};
