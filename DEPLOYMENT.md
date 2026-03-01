# Deployment Guide for Streamlit Cloud

## Problem: Model File Too Large

The trained model file (`model.safetensors` - 255 MB) exceeds GitHub's file size limit (100 MB), so it cannot be included in the repository.

## Solution Options

### Option 1: Upload Model to Hugging Face (Recommended)

1. **Create a Hugging Face Account**
   - Go to https://huggingface.co/
   - Sign up for a free account

2. **Upload Your Model**
   ```bash
   # Install huggingface_hub
   pip install huggingface_hub
   
   # Login to Hugging Face
   huggingface-cli login
   
   # Upload your model
   huggingface-cli upload your-username/cyberbullying-detector ./data/cyberbullying_model_balanced
   ```

3. **Update app.py**
   Replace the model loading code with:
   ```python
   model = DistilBertForSequenceClassification.from_pretrained("your-username/cyberbullying-detector")
   tokenizer = DistilBertTokenizer.from_pretrained("your-username/cyberbullying-detector")
   ```

### Option 2: Use Git LFS (Large File Storage)

1. **Install Git LFS**
   ```bash
   git lfs install
   ```

2. **Track Large Files**
   ```bash
   git lfs track "data/cyberbullying_model_balanced/model.safetensors"
   git lfs track "*.safetensors"
   ```

3. **Add and Commit**
   ```bash
   git add .gitattributes
   git add data/cyberbullying_model_balanced/model.safetensors
   git commit -m "Add model with Git LFS"
   git push
   ```

### Option 3: Use Base Model (Current Fallback)

The app is currently configured to use the base `distilbert-base-uncased` model if your fine-tuned model is not found. This will work but with lower accuracy.

**Note**: The base model is NOT trained on cyberbullying data, so predictions will be random/inaccurate.

## Recommended Deployment Steps

1. **Upload model to Hugging Face** (Best option)
2. **Update app.py** with your Hugging Face model path
3. **Push changes to GitHub**
4. **Deploy on Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repository
   - Set main file: `app.py`
   - Click "Deploy"

## Environment Variables (Optional)

If you want to keep your model private, you can use Streamlit secrets:

1. In Streamlit Cloud, go to App Settings → Secrets
2. Add:
   ```toml
   HUGGINGFACE_TOKEN = "your_hf_token"
   MODEL_NAME = "your-username/cyberbullying-detector"
   ```

3. Update app.py to use secrets:
   ```python
   import streamlit as st
   model_name = st.secrets.get("MODEL_NAME", "distilbert-base-uncased")
   ```

## Current Status

✅ App will deploy and run  
⚠️ Using base DistilBERT model (not fine-tuned)  
❌ Predictions will not be accurate without the trained model  

**Action Required**: Upload your trained model to Hugging Face for accurate predictions!
