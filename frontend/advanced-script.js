// API Configuration
const API_URL = 'http://127.0.0.1:8000/predict';

// DOM Elements
const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const charCountBar = document.getElementById('charCountBar');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingContainer = document.getElementById('loadingContainer');
const resultContainer = document.getElementById('resultContainer');
const statusBadge = document.getElementById('statusBadge');
const predictionText = document.getElementById('predictionText');
const confidenceBar = document.getElementById('confidenceBar');
const confidenceText = document.getElementById('confidenceText');
const detailedPrediction = document.getElementById('detailedPrediction');
const insightBox = document.getElementById('insightBox');
const analyzeAgainBtn = document.getElementById('analyzeAgainBtn');

// Particle Canvas Setup
const canvas = document.getElementById('particlesCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = canvas.height + Math.random() * 100;
        this.size = Math.random() * 3 + 1;
        this.speedY = Math.random() * 1 + 0.5;
        this.speedX = Math.random() * 0.5 - 0.25;
        this.opacity = Math.random() * 0.5 + 0.2;
    }
    
    update() {
        this.y -= this.speedY;
        this.x += this.speedX;
        
        if (this.y < -10) {
            this.y = canvas.height + 10;
            this.x = Math.random() * canvas.width;
        }
    }
    
    draw() {
        ctx.fillStyle = `rgba(102, 126, 234, ${this.opacity})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

const particles = [];
for (let i = 0; i < 100; i++) {
    particles.push(new Particle());
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });
    
    requestAnimationFrame(animateParticles);
}

animateParticles();

// Resize canvas on window resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// Animate stat numbers on load
function animateStatNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const target = parseFloat(stat.getAttribute('data-target'));
        if (isNaN(target)) return;
        
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                stat.textContent = target % 1 === 0 ? target : target.toFixed(1);
                clearInterval(timer);
            } else {
                stat.textContent = current % 1 === 0 ? Math.floor(current) : current.toFixed(1);
            }
        }, 30);
    });
}

// Run on page load
window.addEventListener('load', () => {
    setTimeout(animateStatNumbers, 500);
});

// Character counter with bar
textInput.addEventListener('input', () => {
    const length = textInput.value.length;
    const maxLength = 500;
    const percentage = (length / maxLength) * 100;
    
    charCount.textContent = length;
    charCountBar.style.width = `${percentage}%`;
    
    if (length > 450) {
        charCountBar.style.background = 'linear-gradient(90deg, #f56565, #c53030)';
        charCount.style.color = '#f56565';
    } else if (length > 0) {
        charCountBar.style.background = 'linear-gradient(90deg, #667eea, #764ba2)';
        charCount.style.color = '#667eea';
    } else {
        charCountBar.style.width = '0';
        charCount.style.color = '#718096';
    }
});

// Analyze button click
analyzeBtn.addEventListener('click', async () => {
    const text = textInput.value.trim();
    
    if (!text) {
        showNotification('Please enter some text to analyze', 'warning');
        return;
    }
    
    if (text.length > 500) {
        showNotification('Text is too long. Maximum 500 characters allowed.', 'error');
        return;
    }
    
    await analyzeText(text);
});

// Enter key to submit (Ctrl+Enter)
textInput.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        analyzeBtn.click();
    }
});

// Analyze text function
async function analyzeText(text) {
    // Show loading
    analyzeBtn.disabled = true;
    resultContainer.classList.add('hidden');
    loadingContainer.classList.remove('hidden');
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to analyze text');
        }
        
        const data = await response.json();
        
        // Delay for effect
        setTimeout(() => {
            displayResult(data);
        }, 800);
        
    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message || 'Failed to connect to the server. Make sure the backend is running.', 'error');
        loadingContainer.classList.add('hidden');
    } finally {
        analyzeBtn.disabled = false;
    }
}

// Display result
function displayResult(data) {
    const { prediction, detailed_prediction, confidence } = data;
    
    loadingContainer.classList.add('hidden');
    
    // Set prediction text
    predictionText.textContent = prediction;
    detailedPrediction.textContent = detailed_prediction;
    
    // Set confidence
    confidenceText.textContent = `${confidence}%`;
    
    // Set confidence percentage in simple display
    const confidencePercentage = document.getElementById('confidencePercentage');
    if (confidencePercentage) {
        // Animate the number counting up
        let current = 0;
        const target = confidence;
        const increment = target / 30;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                confidencePercentage.textContent = target.toFixed(1);
                clearInterval(timer);
            } else {
                confidencePercentage.textContent = current.toFixed(1);
            }
        }, 30);
    }
    
    // Set status badge
    const iconMap = {
        'Normal': '✅',
        'Toxic': '⚠️',
        'Hate Speech': '🚫',
        'Threat': '⛔'
    };
    
    const icon = iconMap[prediction] || '🔍';
    let badgeClass = '';
    
    switch (prediction.toLowerCase()) {
        case 'normal':
            badgeClass = 'status-normal';
            break;
        case 'toxic':
            badgeClass = 'status-toxic';
            break;
        case 'hate speech':
            badgeClass = 'status-hate';
            break;
        case 'threat':
            badgeClass = 'status-threat';
            break;
    }
    
    statusBadge.innerHTML = `<div class="status-badge ${badgeClass}">${icon} ${prediction.toUpperCase()}</div>`;
    
    // Set insight
    let insightHTML = '';
    switch (prediction.toLowerCase()) {
        case 'normal':
            insightHTML = '<p>✅ <strong>Safe Content:</strong> This text appears to be safe and non-threatening. No harmful content detected.</p>';
            break;
        case 'toxic':
            insightHTML = '<p>⚠️ <strong>Toxic Content:</strong> This text contains toxic or insulting language. Consider moderating this content.</p>';
            break;
        case 'hate speech':
            insightHTML = '<p>🚫 <strong>Hate Speech Detected:</strong> This text contains hate speech. Immediate action recommended.</p>';
            break;
        case 'threat':
            insightHTML = '<p>⛔ <strong>Threat Detected:</strong> This text contains threatening language. Urgent action required!</p>';
            break;
    }
    insightBox.innerHTML = insightHTML;
    
    // Show result
    resultContainer.classList.remove('hidden');
    
    // Scroll to result
    setTimeout(() => {
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 300);
}

// Show notification
function showNotification(message, type = 'info') {
    const colors = {
        info: 'rgba(102, 126, 234, 0.9)',
        warning: 'rgba(237, 137, 54, 0.9)',
        error: 'rgba(245, 101, 101, 0.9)',
        success: 'rgba(72, 187, 120, 0.9)'
    };
    
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type]};
        color: white;
        padding: 20px 30px;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        z-index: 10000;
        animation: slideInRight 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        max-width: 400px;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        backdrop-filter: blur(10px);
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => notification.remove(), 500);
    }, 4000);
}

// Analyze again button
analyzeAgainBtn.addEventListener('click', () => {
    textInput.value = '';
    charCount.textContent = '0';
    charCountBar.style.width = '0';
    resultContainer.classList.add('hidden');
    textInput.focus();
    
    // Scroll to input
    textInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
});

// Add animations CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Focus on input on load
window.addEventListener('load', () => {
    textInput.focus();
});

// Add button ripple effect
analyzeBtn.addEventListener('click', function(e) {
    const ripple = document.createElement('span');
    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        left: ${x}px;
        top: ${y}px;
        pointer-events: none;
        animation: rippleEffect 0.6s ease-out;
    `;
    
    this.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
});

const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes rippleEffect {
        from {
            transform: scale(0);
            opacity: 1;
        }
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);
