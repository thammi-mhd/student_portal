/**
 * Check if the user is authenticated.
 * @returns {boolean} True if token exists.
 */
function checkAuth() {
    return !!localStorage.getItem('auth_token');
}

/**
 * Protect page logic. Redirects to login if unauthenticated.
 */
function requireAuth() {
    if (!checkAuth()) {
        window.location.href = 'login.html';
    }
}

/**
 * Redirects to dashboard if user is already authenticated.
 */
function redirectIfAuth() {
    if (checkAuth()) {
        window.location.href = 'dashboard.html';
    }
}

/**
 * Perform logout logic.
 */
function logout() {
    localStorage.removeItem('auth_token');
    window.location.href = 'login.html';
}

/**
 * Save the token.
 * @param {string} token 
 */
function setAuthToken(token) {
    localStorage.setItem('auth_token', token);
}

// Utility for Alert Handling
function showAlert(alertElementId, message, type = 'error') {
    const alertEl = document.getElementById(alertElementId);
    if (alertEl) {
        alertEl.style.display = 'block';
        alertEl.textContent = message;
        alertEl.className = `alert alert-${type}`;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            alertEl.style.display = 'none';
        }, 5000);
    }
}
