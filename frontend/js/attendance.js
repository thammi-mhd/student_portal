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
    const fileInput = document.getElementById('attendImage');
    const imgPreview = document.getElementById('attendImagePreview');
    const uploadText = document.getElementById('attendUploadText');

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
            uploadText.textContent = 'Click or drag an image here to scan a face.';
            imgPreview.style.display = 'none';
            imgPreview.src = '';
        }
    });

    // Handle Mark Attendance Form Submission
    const markAttendanceForm = document.getElementById('markAttendanceForm');
    const recognitionResult = document.getElementById('recognitionResult');
    const resultTitle = document.getElementById('resultTitle');
    const resultContent = document.getElementById('resultContent');

    markAttendanceForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('markAttendanceBtn');
        btn.textContent = 'Processing...';
        btn.disabled = true;
        recognitionResult.style.display = 'none';

        const file = document.getElementById('attendImage').files[0];
        const formData = new FormData();
        
        // Using common keys for file uploads in Flask
        formData.append('image', file);
        formData.append('file', file);

        try {
            const response = await api.markAttendance(formData);
            
            // Checks for success flags commonly used in endpoints like this
            const recognized = response.recognized !== undefined ? response.recognized : !!response.student;

            recognitionResult.style.display = 'block';

            if (recognized || response.success) {
                resultTitle.textContent = "Attendance Marked Successfully";
                resultTitle.style.color = "var(--accent)";
                
                const studentName = response.student?.name || response.name || response.student_name || 'Unknown Student';
                const rollNo = response.student?.roll_number || response.roll_number || 'N/A';

                resultContent.innerHTML = `
                    <div style="background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 6px; border-left: 4px solid var(--accent); margin-bottom: 0.5rem;">
                        <p style="margin-bottom: 0.25rem;"><strong>Student Recognized:</strong> ${studentName}</p>
                        <p><strong>Roll Number / ID:</strong> ${rollNo}</p>
                    </div>
                    <p style="color: var(--text-muted); font-size: 0.75rem;">Attendance recorded on database.</p>
                `;
                
                // Automatically refresh historical records
                fetchAttendance();
            } else {
                resultTitle.textContent = "Student Not Recognized";
                resultTitle.style.color = "var(--danger)";
                resultContent.innerHTML = `
                    <div style="background: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 6px; border-left: 4px solid var(--danger);">
                        <p>${response.message || 'No matching student face profile found. Please try again with clearer lighting or re-register the student image.'}</p>
                    </div>
                `;
            }

        } catch (error) {
            showAlert('attendanceAlert', error.message || 'Error communicating with attendance server.', 'error');
            
            // Show result block with error
            recognitionResult.style.display = 'block';
            resultTitle.textContent = "Processing Error";
            resultTitle.style.color = "var(--danger)";
            resultContent.innerHTML = `<p>${error.message || 'An unexpected error occurred parsing the facial features.'}</p>`;
        } finally {
            btn.textContent = 'Scan & Mark Attendance';
            btn.disabled = false;
        }
    });

    // Load Initial Data
    fetchAttendance();
});

// Attach fetch method to window to be accessible by html inline handlers
window.fetchAttendance = async function() {
    const tbody = document.getElementById('attendanceTableBody');
    tbody.innerHTML = '<tr><td colspan="4" class="text-center">Loading records...</td></tr>';
    
    try {
        const response = await api.getAttendance();
        let records = [];
        
        if (Array.isArray(response)) {
            records = response;
        } else if (response && response.data) {
            records = response.data;
        } else if (response && response.attendance) {
            records = response.attendance;
        }

        if (records.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center" style="color: var(--text-muted);">No attendance records found yet.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        records.forEach(record => {
            const tr = document.createElement('tr');
            
            const sName = record.student_name || record.name || 'Unknown';
            const sRoll = record.roll_number || record.student_id || 'N/A';
            const dateStr = record.timestamp || record.date || 'N/A';
            let formattedDate = dateStr;
            let formattedTime = record.time || 'N/A';

            // Auto format dates if wrapped as DateTime string from SQL
            if (dateStr.includes('T') && dateStr.length > 10) {
                const dateObj = new Date(dateStr);
                formattedDate = dateObj.toLocaleDateString();
                formattedTime = dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            }

            tr.innerHTML = `
                <td style="font-weight: 500;">${sName}</td>
                <td>${sRoll}</td>
                <td>${formattedDate}</td>
                <td>${formattedTime}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Fetch attendance error:", error);
        tbody.innerHTML = `<tr><td colspan="4" class="text-center" style="color: var(--danger);">Failed to load records. ${error.message}</td></tr>`;
    }
};
