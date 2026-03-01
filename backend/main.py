from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import re
import nltk
from nltk.corpus import stopwords
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os

# Download stopwords
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

app = FastAPI(title="Cyberbullying Detection API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and tokenizer
model = None
tokenizer = None
stop_words = set(stopwords.words('english'))

# Label mapping
labels_map = {
    0: "Normal",
    1: "Toxic",
    2: "Obscene",
    3: "Severe Toxic",
    4: "Hate Speech",
    5: "Threat"
}

# Simplified category mapping for frontend
category_map = {
    "Normal": "Normal",
    "Toxic": "Toxic",
    "Obscene": "Toxic",
    "Severe Toxic": "Toxic",
    "Hate Speech": "Hate Speech",
    "Threat": "Threat"
}

def clean_text(text: str) -> str:
    """Clean and preprocess text"""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    words = text.split()
    words = [word for word in words if word not in stop_words]
    
    return " ".join(words)

@app.on_event("startup")
async def load_model():
    """Load model on startup"""
    global model, tokenizer
    
    try:
        model_path = "../data/cyberbullying_model_balanced"
        
        if not os.path.exists(model_path):
            model_path = "data/cyberbullying_model_balanced"
        
        print(f"Loading model from: {model_path}")
        model = DistilBertForSequenceClassification.from_pretrained(model_path)
        tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        model.eval()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

class TextInput(BaseModel):
    text: str

class PredictionOutput(BaseModel):
    prediction: str
    detailed_prediction: str
    confidence: float
    cleaned_text: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "online", "message": "Cyberbullying Detection API"}

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: TextInput):
    """Predict cyberbullying category"""
    try:
        if not input_data.text or len(input_data.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Clean text
        cleaned_text = clean_text(input_data.text)
        
        if len(cleaned_text.strip()) == 0:
            cleaned_text = input_data.text.lower()
        
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
        
        return {
            "prediction": simplified_prediction,
            "detailed_prediction": detailed_prediction,
            "confidence": round(confidence * 100, 2),
            "cleaned_text": cleaned_text
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
