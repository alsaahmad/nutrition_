/**
 * Nutrition Track - JavaScript
 * Google Cloud Vision API Integration
 */

// DOM Elements
const authPage = document.getElementById('auth-page');
const mainPage = document.getElementById('main-page');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const showSignupLink = document.getElementById('show-signup');
const showLoginLink = document.getElementById('show-login');
const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');
const logoutBtn = document.getElementById('logout-btn');
const uploadBox = document.getElementById('upload-box');
const fileInput = document.getElementById('file-input');
const imagePreview = document.getElementById('image-preview');
const previewImg = document.getElementById('preview-img');
const changeImageBtn = document.getElementById('change-image');
const analyzeBtn = document.getElementById('analyze-btn');
const analyzeText = document.getElementById('analyze-text');
const analyzeLoader = document.getElementById('analyze-loader');
const resultsSection = document.getElementById('results-section');
const foodNameEl = document.getElementById('food-name');
const detectedLabelsEl = document.getElementById('detected-labels');
const caloriesEl = document.getElementById('calories');
const proteinEl = document.getElementById('protein');
const carbsEl = document.getElementById('carbs');
const fatsEl = document.getElementById('fats');
const tipTextEl = document.getElementById('tip-text');
const greetingContainer = document.getElementById('greeting-container');
const greetingText = document.getElementById('greeting-text');

// State
let currentFile = null;

// Check login status
function isLoggedIn() {
    return localStorage.getItem('nutritiontrack_user') !== null;
}

// Get User Name
function getUserName() {
    const userStr = localStorage.getItem('nutritiontrack_user');
    if (userStr) {
        try {
            const user = JSON.parse(userStr);
            return user.name || 'User';
        } catch (e) {
            return 'User';
        }
    }
    return 'User';
}

// Update Greeting based on time
function updateGreeting() {
    const name = getUserName();
    const now = new Date();
    const hour = now.getHours();
    
    let greeting = '';
    let emoji = '';

    if (hour >= 5 && hour < 12) {
        greeting = 'Good Morning';
        emoji = '☀️';
    } else if (hour >= 12 && hour < 17) {
        greeting = 'Good Afternoon';
        emoji = '🌤️';
    } else if (hour >= 17 && hour < 21) {
        greeting = 'Good Evening';
        emoji = '🌆';
    } else {
        greeting = 'Good Night';
        emoji = '🌙';
    }

    greetingText.innerHTML = `${greeting}, <span class="bg-gradient-to-r from-accent to-green-400 bg-clip-text text-transparent">${name}</span> ${emoji}`;
    
    // Animate greeting
    setTimeout(() => {
        greetingContainer.classList.remove('opacity-0', 'translate-y-4');
        greetingContainer.classList.add('opacity-100', 'translate-y-0');
    }, 100);
}

// Show appropriate screen
function showAppropriateScreen() {
    if (isLoggedIn()) {
        authPage.classList.add('hidden');
        mainPage.classList.remove('hidden');
        setTimeout(updateGreeting, 100);
    } else {
        authPage.classList.remove('hidden');
        mainPage.classList.add('hidden');
    }
}

// Toggle auth forms
function toggleAuthForms(showLogin) {
    if (showLogin) {
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
    } else {
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
    }
}

// Handle Login
function handleLogin() {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    const name = email.split('@')[0];
    const formattedName = name.charAt(0).toUpperCase() + name.slice(1);

    localStorage.setItem('nutritiontrack_user', JSON.stringify({ email, name: formattedName }));
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
    
    showNotification('Welcome back!', 'success');
    showAppropriateScreen();
}

// Handle Signup
function handleSignup() {
    const name = document.getElementById('signup-name').value.trim();
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;

    if (!name || !email || !password) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    if (password.length < 6) {
        showNotification('Password must be at least 6 characters', 'error');
        return;
    }

    localStorage.setItem('nutritiontrack_user', JSON.stringify({ email, name }));
    document.getElementById('signup-name').value = '';
    document.getElementById('signup-email').value = '';
    document.getElementById('signup-password').value = '';
    
    showNotification('Account created successfully!', 'success');
    showAppropriateScreen();
}

// Handle Logout
function handleLogout() {
    localStorage.removeItem('nutritiontrack_user');
    resetUploadState();
    showNotification('Logged out successfully', 'success');
    showAppropriateScreen();
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-xl shadow-lg transition-all transform translate-x-full ${
        type === 'success' ? 'bg-accent text-black' : 
        type === 'error' ? 'bg-red-500 text-white' : 
        'bg-dark-card border border-dark-border text-white'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
        notification.classList.add('translate-x-0');
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('translate-x-0');
        notification.classList.add('translate-x-full');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        showNotification('Please select an image file', 'error');
        return;
    }

    currentFile = file;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImg.src = e.target.result;
        uploadBox.classList.add('hidden');
        imagePreview.classList.remove('hidden');
        analyzeBtn.disabled = false;
        resultsSection.classList.add('hidden', 'opacity-0', 'translate-y-4');
    };
    reader.readAsDataURL(file);
}

// Reset upload state
function resetUploadState() {
    currentFile = null;
    fileInput.value = '';
    uploadBox.classList.remove('hidden');
    imagePreview.classList.add('hidden');
    resultsSection.classList.add('hidden', 'opacity-0', 'translate-y-4');
    analyzeBtn.disabled = true;
}

// Setup drag and drop
function setupDragAndDrop() {
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('border-accent', 'bg-dark-hover');
    });

    uploadBox.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('border-accent', 'bg-dark-hover');
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('border-accent', 'bg-dark-hover');
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect({ target: fileInput });
        }
    });
}

// Analyze image using backend API
async function analyzeImage() {
    if (!currentFile) {
        showNotification('Please select an image first', 'error');
        return;
    }

    // Loading state
    analyzeBtn.disabled = true;
    analyzeText.textContent = 'Analyzing with AI...';
    analyzeLoader.classList.remove('hidden');
    resultsSection.classList.add('hidden', 'opacity-0', 'translate-y-4');

    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', currentFile);

        // Call backend API
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Analysis failed');
        }

        const data = await response.json();
        
        // Display results
        displayResults(data);
        showNotification('Analysis complete!', 'success');

    } catch (error) {
        console.error('Analysis error:', error);
        showNotification(error.message || 'Failed to analyze image. Please try again.', 'error');
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        analyzeText.textContent = 'Analyze Nutrition';
        analyzeLoader.classList.add('hidden');
    }
}

// Display results with animation
function displayResults(data) {
    // Update nutrition data
    foodNameEl.textContent = data.food_name || 'Unknown Food';
    caloriesEl.textContent = data.calories || '--';
    proteinEl.textContent = data.protein || '--';
    carbsEl.textContent = data.carbs || '--';
    fatsEl.textContent = data.fats || '--';
    tipTextEl.textContent = data.health_tip || 'Enjoy your meal!';
    
    // Update detected labels
    if (data.detected_labels && data.detected_labels.length > 0) {
        detectedLabelsEl.textContent = `Detected items: ${data.detected_labels.join(', ')}`;
    } else {
        detectedLabelsEl.textContent = 'Detected items: Multiple food items';
    }

    // Show results with animation
    resultsSection.classList.remove('hidden');
    
    setTimeout(() => {
        resultsSection.classList.remove('opacity-0', 'translate-y-4');
        resultsSection.classList.add('opacity-100', 'translate-y-0');
        
        // Smooth scroll
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Event Listeners
showSignupLink.addEventListener('click', (e) => { 
    e.preventDefault(); 
    toggleAuthForms(false); 
});

showLoginLink.addEventListener('click', (e) => { 
    e.preventDefault(); 
    toggleAuthForms(true); 
});

loginBtn.addEventListener('click', handleLogin);
signupBtn.addEventListener('click', handleSignup);
logoutBtn.addEventListener('click', handleLogout);
uploadBox.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
changeImageBtn.addEventListener('click', resetUploadState);
analyzeBtn.addEventListener('click', analyzeImage);

// Enter key support for forms
document.getElementById('login-password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleLogin();
});

document.getElementById('signup-password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSignup();
});

// Initialize
setupDragAndDrop();
showAppropriateScreen();
