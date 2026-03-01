import streamlit as st
import torch
import re
import nltk
from nltk.corpus import stopwords
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os
import time

# Page config
st.set_page_config(
    page_title="Cyberbullying Detection AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Advanced Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Particle effect background */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 0;
        pointer-events: none;
    }
    
    .particle {
        position: absolute;
        width: 3px;
        height: 3px;
        background: rgba(102, 126, 234, 0.5);
        border-radius: 50%;
        animation: float 20s infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) translateX(100px); opacity: 0; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* Animated Title with Glow */
    .main-title {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 72px;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        animation: titleGlow 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        letter-spacing: 3px;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: brightness(1) drop-shadow(0 0 20px rgba(102, 126, 234, 0.5)); }
        50% { filter: brightness(1.3) drop-shadow(0 0 40px rgba(118, 75, 162, 0.8)); }
    }
    
    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 20px;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 50px;
        animation: fadeInUp 1s ease;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Stats Dashboard */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 30px 0;
        gap: 20px;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        flex: 1;
        transition: all 0.3s ease;
        animation: slideIn 0.8s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .stat-number {
        font-size: 42px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', sans-serif;
    }
    
    .stat-label {
        color: #a0aec0;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    
    /* Advanced Input Card */
    .input-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 40px;
        margin: 30px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: fadeIn 1s ease;
        position: relative;
        overflow: hidden;
    }
    
    .input-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        color: white !important;
        font-size: 18px !important;
        font-family: 'Poppins', sans-serif !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.5) !important;
        background: rgba(255, 255, 255, 0.12) !important;
        transform: scale(1.01);
    }
    
    /* Advanced Button with Ripple Effect */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 20px;
        font-weight: 700;
        padding: 20px;
        border-radius: 20px;
        border: none;
        transition: all 0.4s ease;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
        box-shadow: 0 5px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.6);
    }
    
    .stButton button:active {
        transform: translateY(-2px) scale(0.98);
    }
    
    /* Advanced Result Cards with 3D Effect */
    .result-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 40px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        margin: 30px 0;
        animation: resultAppear 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4);
        transform-style: preserve-3d;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-10px) rotateX(2deg);
        box-shadow: 0 25px 70px rgba(102, 126, 234, 0.4);
    }
    
    @keyframes resultAppear {
        0% {
            opacity: 0;
            transform: scale(0.5) rotateY(180deg);
        }
        100% {
            opacity: 1;
            transform: scale(1) rotateY(0deg);
        }
    }
    
    /* Status Badges with Pulse Animation */
    .status-normal {
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.3), rgba(56, 161, 105, 0.3));
        color: #48bb78;
        border: 3px solid #48bb78;
        padding: 15px 35px;
        border-radius: 25px;
        font-weight: 700;
        text-align: center;
        font-size: 24px;
        font-family: 'Orbitron', sans-serif;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(72, 187, 120, 0.5);
        letter-spacing: 2px;
    }
    
    .status-toxic {
        background: linear-gradient(135deg, rgba(237, 137, 54, 0.3), rgba(221, 107, 32, 0.3));
        color: #ed8936;
        border: 3px solid #ed8936;
        padding: 15px 35px;
        border-radius: 25px;
        font-weight: 700;
        text-align: center;
        font-size: 24px;
        font-family: 'Orbitron', sans-serif;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(237, 137, 54, 0.5);
        letter-spacing: 2px;
    }
    
    .status-hate {
        background: linear-gradient(135deg, rgba(245, 101, 101, 0.3), rgba(229, 62, 62, 0.3));
        color: #f56565;
        border: 3px solid #f56565;
        padding: 15px 35px;
        border-radius: 25px;
        font-weight: 700;
        text-align: center;
        font-size: 24px;
        font-family: 'Orbitron', sans-serif;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(245, 101, 101, 0.5);
        letter-spacing: 2px;
    }
    
    .status-threat {
        background: linear-gradient(135deg, rgba(197, 48, 48, 0.3), rgba(155, 44, 44, 0.3));
        color: #c53030;
        border: 3px solid #c53030;
        padding: 15px 35px;
        border-radius: 25px;
        font-weight: 700;
        text-align: center;
        font-size: 24px;
        font-family: 'Orbitron', sans-serif;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(197, 48, 48, 0.5);
        letter-spacing: 2px;
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 0 30px currentColor;
        }
        50% {
            transform: scale(1.05);
            box-shadow: 0 0 50px currentColor;
        }
    }
    
    /* Metric Cards with Hover Effect */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
        padding: 30px;
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        margin: 15px 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateX(10px);
        border-color: #667eea;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .metric-label {
        color: #a0aec0;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 15px;
        font-family: 'Orbitron', sans-serif;
    }
    
    .metric-value {
        color: white;
        font-size: 32px;
        font-weight: 700;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Progress Bar Animation */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 100%;
        animation: progressShine 2s linear infinite;
        border-radius: 10px;
        height: 15px !important;
    }
    
    @keyframes progressShine {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-top-color: #667eea !important;
        border-right-color: #764ba2 !important;
        border-bottom-color: #f093fb !important;
    }
    
    /* Columns */
    .stColumn {
        padding: 10px;
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        color: #e2e8f0;
        animation: slideInLeft 0.8s ease;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
</style>
""", unsafe_allow_html=True)

# Download stopwords
@st.cache_resource
def download_stopwords():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    return set(stopwords.words('english'))

# Load model
@st.cache_resource
def load_model():
    """Load the DistilBERT model"""
    try:
        # Try loading from local path first
        model_path = "data/cyberbullying_model_balanced"
        
        if os.path.exists(model_path) and os.path.exists(os.path.join(model_path, "model.safetensors")):
            model = DistilBertForSequenceClassification.from_pretrained(model_path)
            tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        else:
            # Fallback: Load base DistilBERT model (not fine-tuned)
            st.warning("⚠️ Using base DistilBERT model. For best results, upload your fine-tuned model to Hugging Face.")
            model = DistilBertForSequenceClassification.from_pretrained(
                "distilbert-base-uncased",
                num_labels=6
            )
            tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        
        model.eval()
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# Clean text function
def clean_text(text, stop_words):
    """Clean and preprocess text"""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    words = text.split()
    words = [word for word in words if word not in stop_words]
    
    return " ".join(words)

# Label mappings
labels_map = {
    0: "Normal",
    1: "Toxic",
    2: "Obscene",
    3: "Severe Toxic",
    4: "Hate Speech",
    5: "Threat"
}

category_map = {
    "Normal": "Normal",
    "Toxic": "Toxic",
    "Obscene": "Toxic",
    "Severe Toxic": "Toxic",
    "Hate Speech": "Hate Speech",
    "Threat": "Threat"
}

# Main app
def main():
    # Particle background effect
    st.markdown("""
    <div class="particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 1s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 3s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 5s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 2.5s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 4.5s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 1.5s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Header with enhanced styling
    st.markdown('<h1 class="main-title">🛡️ CYBERBULLYING DETECTION AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">⚡ Advanced Neural Network Analysis • Real-Time Protection ⚡</p>', unsafe_allow_html=True)
    
    # Stats Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">91.30%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">6</div>
            <div class="stat-label">Categories</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">&lt;1s</div>
            <div class="stat-label">Response Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">DistilBERT</div>
            <div class="stat-label">Model</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Load resources
    stop_words = download_stopwords()
    model, tokenizer = load_model()
    
    if model is None or tokenizer is None:
        st.error("⚠️ Failed to load model. Please check the model path.")
        return
    
    # Input section with container
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    st.markdown("### 📝 Enter Text for Analysis")
    st.markdown('<div class="info-box">💡 Tip: Enter any text to analyze for cyberbullying, hate speech, threats, or toxic content. Our AI model will classify it in real-time.</div>', unsafe_allow_html=True)
    
    text_input = st.text_area(
        "",
        placeholder="Type or paste text here to check for cyberbullying, hate speech, or threats...\n\nExample: 'You are amazing!' or 'I hate you and will hurt you'",
        height=180,
        max_chars=500,
        label_visibility="collapsed"
    )
    
    # Character count with styling
    char_count = len(text_input)
    color = "#f56565" if char_count > 450 else "#667eea" if char_count > 0 else "#718096"
    st.markdown(f"<p style='text-align: right; color: {color}; font-size: 14px; font-weight: 600; font-family: Orbitron;'>⌨️ {char_count} / 500 characters</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button("🔍 ANALYZE TEXT", use_container_width=True)
    
    if analyze_clicked:
        if not text_input.strip():
            st.warning("⚠️ Please enter some text to analyze")
            return
        
        # Show loading with custom message
        with st.spinner("🔄 AI Model Processing... Analyzing patterns and context..."):
            time.sleep(0.5)  # Brief pause for effect
            
            try:
                # Clean text
                cleaned_text = clean_text(text_input, stop_words)
                
                if len(cleaned_text.strip()) == 0:
                    cleaned_text = text_input.lower()
                
                # Tokenize
                inputs = tokenizer(cleaned_text, return_tensors="pt", truncation=True, max_length=512)
                
                # Predict
                with torch.no_grad():
                    outputs = model(**inputs)
                    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
                    prediction_idx = torch.argmax(probabilities).item()
                    confidence = probabilities[0][prediction_idx].item()
                
                detailed_prediction = labels_map[prediction_idx]
                simplified_prediction = category_map[detailed_prediction]
                
                # Display results with animation
                st.markdown("---")
                st.markdown("### 🎯 ANALYSIS RESULTS")
                
                # Status badge with icon
                icon_map = {
                    "Normal": "✅",
                    "Toxic": "⚠️",
                    "Hate Speech": "🚫",
                    "Threat": "⛔"
                }
                
                icon = icon_map.get(simplified_prediction, "🔍")
                
                if simplified_prediction == "Normal":
                    st.markdown(f'<div class="status-normal">{icon} {simplified_prediction.upper()}</div>', unsafe_allow_html=True)
                elif simplified_prediction == "Toxic":
                    st.markdown(f'<div class="status-toxic">{icon} {simplified_prediction.upper()}</div>', unsafe_allow_html=True)
                elif simplified_prediction == "Hate Speech":
                    st.markdown(f'<div class="status-hate">{icon} {simplified_prediction.upper()}</div>', unsafe_allow_html=True)
                elif simplified_prediction == "Threat":
                    st.markdown(f'<div class="status-threat">{icon} {simplified_prediction.upper()}</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Metrics in columns with enhanced styling
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">🎯 Classification</div>
                        <div class="metric-value">{simplified_prediction}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📊 Confidence Score</div>
                        <div class="metric-value">{confidence * 100:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detailed prediction
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🔬 Detailed Category</div>
                    <div class="metric-value" style="font-size: 24px;">{detailed_prediction}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Confidence percentage - simple black and white
                st.markdown("""
                <div style="background: white; padding: 30px; border-radius: 15px; margin: 20px 0;">
                    <div style="color: black; font-size: 18px; font-weight: 600; margin-bottom: 10px;">
                        Confidence Level
                    </div>
                    <div style="color: black; font-size: 48px; font-weight: 700; font-family: 'Orbitron', monospace;">
                        {:.1f}%
                    </div>
                </div>
                """.format(confidence * 100), unsafe_allow_html=True)
                
                # Additional insights
                st.markdown("---")
                st.markdown("### 💡 Insights")
                
                if simplified_prediction == "Normal":
                    st.success("✅ This text appears to be safe and non-threatening. No harmful content detected.")
                elif simplified_prediction == "Toxic":
                    st.warning("⚠️ This text contains toxic or insulting language. Consider moderating this content.")
                elif simplified_prediction == "Hate Speech":
                    st.error("🚫 This text contains hate speech. Immediate action recommended.")
                elif simplified_prediction == "Threat":
                    st.error("⛔ This text contains threatening language. Urgent action required!")
                
                # Show all probabilities - simple table format
                with st.expander("📈 View All Category Probabilities"):
                    # Create a clean table display
                    import pandas as pd
                    
                    prob_data = []
                    for idx, label in labels_map.items():
                        prob = probabilities[0][idx].item()
                        prob_data.append({
                            'Category': label,
                            'Probability': f'{prob * 100:.2f}%'
                        })
                    
                    df = pd.DataFrame(prob_data)
                    
                    # Display as a simple table
                    st.dataframe(
                        df,
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            "Category": st.column_config.TextColumn(
                                "Category",
                                width="medium",
                            ),
                            "Probability": st.column_config.TextColumn(
                                "Probability",
                                width="medium",
                            ),
                        }
                    )
                
            except Exception as e:
                st.error(f"❌ Error during prediction: {str(e)}")
    
    # Footer with enhanced styling
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 30px;'>
        <p style='color: #718096; font-size: 16px; font-family: Orbitron;'>
            ⚡ Powered by DistilBERT Neural Network | Built with Streamlit & PyTorch ⚡
        </p>
        <p style='color: #4a5568; font-size: 14px; margin-top: 10px;'>
            🛡️ AI-Powered Text Analysis for Online Safety
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
