# 🛡️ Cyberbullying Detection - AI-Powered Web Application

A modern, animated web application for detecting cyberbullying, hate speech, and threats using DistilBERT AI model.

## 🌟 Features

- **AI-Powered Detection**: Uses fine-tuned DistilBERT model for accurate classification
- **Modern UI**: Dark gradient theme with glassmorphism effects
- **Smooth Animations**: CSS and JavaScript animations for better UX
- **Real-time Analysis**: Instant text classification
- **Multiple Categories**: Detects Normal, Toxic, Hate Speech, and Threat content
- **Confidence Scores**: Shows prediction confidence percentage
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

```
.
├── backend/
│   └── main.py              # FastAPI backend server
├── frontend/
│   ├── index.html           # Standard HTML UI
│   ├── style.css            # Standard styling
│   ├── script.js            # Standard frontend logic
│   ├── advanced.html        # Advanced UI with particle effects
│   ├── advanced-style.css   # Advanced styling with 3D effects
│   └── advanced-script.js   # Advanced animations & particles
├── data/
│   └── cyberbullying_model_balanced/  # DistilBERT model files
├── app.py                   # Streamlit version (for cloud deployment)
├── requirements.txt         # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Option 1: FastAPI + HTML Frontend (Recommended for Local)

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Download NLTK Data**
```bash
python -c "import nltk; nltk.download('stopwords')"
```

3. **Start Backend Server**
```bash
cd backend
python main.py
```
The API will be available at `http://127.0.0.1:8000`

4. **Open Frontend**

Standard UI:
- Open `frontend/index.html` in your browser

Advanced UI (Recommended):
- Open `frontend/advanced.html` in your browser

Or use a local server:
```bash
cd frontend
python -m http.server 8080
```
Then visit:
- Standard: `http://localhost:8080/index.html`
- Advanced: `http://localhost:8080/advanced.html`

### Option 2: Streamlit (Recommended for Cloud Deployment)

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run Streamlit App**
```bash
streamlit run app.py
```

3. **Deploy to Streamlit Cloud**
- Push your code to GitHub
- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect your repository
- Deploy!

## 🎨 UI Features

### Standard UI (index.html)
- Dark gradient theme with glassmorphism
- Smooth animations and transitions
- Responsive design

### Advanced UI (advanced.html)
- **Particle System**: Animated floating particles using Canvas API
- **3D Card Effects**: Transform and perspective animations
- **Gradient Orbs**: Floating animated background orbs
- **Ripple Effects**: Button click ripple animations
- **Stat Counter**: Animated number counting on page load
- **Progress Bars**: Animated gradient progress indicators
- **Pulse Animations**: Status badges with pulsing glow effects
- **Scan Effects**: Scanning light effects across cards
- **Orbitron Font**: Futuristic typography for tech feel

### Streamlit UI (app.py)
- **Wide Layout**: Full-width responsive design
- **Stats Dashboard**: Real-time metrics display
- **Custom CSS**: Advanced styling within Streamlit
- **Animated Gradients**: Shifting background colors
- **Probability Viewer**: Expandable section showing all category probabilities

### Color Coding
- **Green**: Normal/Safe content
- **Orange**: Toxic content
- **Red**: Hate Speech
- **Dark Red**: Threats

### Animations
- Floating background circles
- Smooth fade-in effects
- Button hover animations
- Loading spinner
- Result card slide-up animation
- Confidence bar fill animation

## 🔧 API Endpoints

### POST `/predict`
Analyze text for cyberbullying content.

**Request:**
```json
{
  "text": "Your text here"
}
```

**Response:**
```json
{
  "prediction": "Normal",
  "detailed_prediction": "Normal",
  "confidence": 95.67,
  "cleaned_text": "cleaned version of text"
}
```

### GET `/`
Health check endpoint.

## 📊 Model Information

- **Model**: DistilBERT for Sequence Classification
- **Categories**: 
  - Normal
  - Toxic / Insult
  - Obscene
  - Severe Toxic
  - Hate Speech
  - Threat

## 🌐 CORS Configuration

The backend is configured to accept requests from any origin. For production, update the CORS settings in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1920px+)
- Laptop (1024px - 1920px)
- Tablet (768px - 1024px)
- Mobile (320px - 768px)

## 🛠️ Technologies Used

### Backend
- FastAPI
- PyTorch
- Transformers (Hugging Face)
- NLTK

### Frontend
- HTML5
- CSS3 (with animations)
- Vanilla JavaScript
- Google Fonts (Poppins)

### Streamlit Version
- Streamlit
- Custom CSS styling

## 🔒 Security Notes

- Input is limited to 500 characters
- Text preprocessing removes URLs and mentions
- Proper error handling for invalid inputs
- CORS protection (configure for production)

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, Streamlit, and DistilBERT**
