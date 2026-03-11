// Configuration
const API_BASE = "http://localhost:5000/api/v1";

// Core Fetch Function
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('auth_token');
    
    if (!options.headers) {
        options.headers = {};
    }
    
    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Automatically set Content-Type to JSON if body is string, otherwise let browser handle FormData
    if (!(options.body instanceof FormData) && !options.headers['Content-Type'] && options.body) {
        options.headers['Content-Type'] = 'application/json';
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        let data;
        
        // Handle empty or text responses
        const text = await response.text();
        try {
            data = text ? JSON.parse(text) : {};
        } catch(e) {
            data = { message: text || "Invalid response format" };
        }
        
        if (!response.ok) {
            throw new Error(data.message || data.error || 'API Request failed');
        }
        
        return data;
    } catch (error) {
        console.error("API Error in request to", endpoint, ":", error);
        throw error;
    }
}

// Global API Object
const api = {
    // Auth endpoints
    loginUser: (credentials) => apiFetch('/auth/login', { method: 'POST', body: JSON.stringify(credentials) }),
    registerUser: (userData) => apiFetch('/auth/register', { method: 'POST', body: JSON.stringify(userData) }),
    
    // Students endpoints
    getStudents: () => apiFetch('/students', { method: 'GET' }),
    createStudent: (formData) => apiFetch('/students/register', { method: 'POST', body: formData }),
    deleteStudent: (id) => apiFetch(`/students/${id}`, { method: 'DELETE' }),
    getDashboardStats: () => apiFetch('/dashboard/stats', { method: 'GET' }),
    
    // Attendance endpoints
    markAttendance: (formData) => apiFetch('/attendance/mark', { method: 'POST', body: formData }),
    getAttendance: () => apiFetch('/admin/attendance', { method: 'GET' })
};
