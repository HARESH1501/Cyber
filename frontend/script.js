// API Configuration
const API_URL = 'http://127.0.0.1:8000/predict';

// DOM Elements
const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingContainer = document.getElementById('loadingContainer');
const resultContainer = document.getElementById('resultContainer');
const statusBadge = document.getElementById('statusBadge');
const predictionText = document.getElementById('predictionText');
const confidenceBar = document.getElementById('confidenceBar');
const confidenceText = document.getElementById('confidenceText');
const detailedPrediction = document.getElementById('detailedPrediction');
const analyzeAgainBtn = document.getElementById('analyzeAgainBtn');

// Character counter
textInput.addEventListener('input', () => {
    const length = textInput.value.length;
    charCount.textContent = length;
    
    if (length > 500) {
        charCount.style.color = '#f56565';
    } else {
        charCount.style.color = '#718096';
    }
});

// Analyze button click
analyzeBtn.addEventListener('click', async () => {
    const text = textInput.value.trim();
    
    if (!text) {
        showError('Please enter some text to analyze');
        return;
    }
    
    if (text.length > 500) {
        showError('Text is too long. Maximum 500 characters allowed.');
        return;
    }
    
    await analyzeText(text);
});

// Enter key to submit
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
        displayResult(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to connect to the server. Make sure the backend is running.');
    } finally {
        analyzeBtn.disabled = false;
        loadingContainer.classList.add('hidden');
    }
}

// Display result
function displayResult(data) {
    const { prediction, detailed_prediction, confidence } = data;
    
    // Set prediction text
    predictionText.textContent = prediction;
    detailedPrediction.textContent = detailed_prediction;
    
    // Set confidence percentage with animation
    const confidencePercentage = document.getElementById('confidencePercentage');
    if (confidencePercentage) {
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
    statusBadge.textContent = prediction;
    statusBadge.className = 'status-badge';
    
    switch (prediction.toLowerCase()) {
        case 'normal':
            statusBadge.classList.add('normal');
            confidenceBar.style.background = 'linear-gradient(90deg, #48bb78 0%, #38a169 100%)';
            break;
        case 'toxic':
            statusBadge.classList.add('toxic');
            confidenceBar.style.background = 'linear-gradient(90deg, #ed8936 0%, #dd6b20 100%)';
            break;
        case 'hate speech':
            statusBadge.classList.add('hate-speech');
            confidenceBar.style.background = 'linear-gradient(90deg, #f56565 0%, #e53e3e 100%)';
            break;
        case 'threat':
            statusBadge.classList.add('threat');
            confidenceBar.style.background = 'linear-gradient(90deg, #c53030 0%, #9b2c2c 100%)';
            break;
    }
    
    // Show result
    resultContainer.classList.remove('hidden');
    
    // Scroll to result
    setTimeout(() => {
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

// Show error
function showError(message) {
    // Create error notification
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(245, 101, 101, 0.9);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    // Remove after 4 seconds
    setTimeout(() => {
        errorDiv.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => errorDiv.remove(), 300);
    }, 4000);
}

// Analyze again button
analyzeAgainBtn.addEventListener('click', () => {
    textInput.value = '';
    charCount.textContent = '0';
    resultContainer.classList.add('hidden');
    textInput.focus();
});

// Add animations CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
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
