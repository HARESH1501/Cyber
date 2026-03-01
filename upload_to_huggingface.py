"""
Script to upload your trained model to Hugging Face Hub
This will make your model accessible from Streamlit Cloud
"""

from huggingface_hub import HfApi, create_repo
from pathlib import Path
import os

# Configuration
MODEL_PATH = "data/cyberbullying_model_balanced"
REPO_NAME = "HARESH1501/cyberbullying-detector"  # Change if needed

def upload_model():
    """Upload model to Hugging Face Hub"""
    
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Error: Model not found at {MODEL_PATH}")
        return
    
    if not os.path.exists(os.path.join(MODEL_PATH, "model.safetensors")):
        print(f"❌ Error: model.safetensors not found in {MODEL_PATH}")
        return
    
    print("🚀 Starting upload to Hugging Face...")
    print(f"📁 Model path: {MODEL_PATH}")
    print(f"📦 Repository: {REPO_NAME}")
    
    try:
        # Initialize API
        api = HfApi()
        
        # Create repository (if it doesn't exist)
        print("\n📝 Creating repository...")
        try:
            create_repo(REPO_NAME, repo_type="model", exist_ok=True)
            print("✅ Repository created/verified")
        except Exception as e:
            print(f"⚠️ Repository might already exist: {e}")
        
        # Upload all files from model directory
        print("\n📤 Uploading model files...")
        api.upload_folder(
            folder_path=MODEL_PATH,
            repo_id=REPO_NAME,
            repo_type="model",
        )
        
        print("\n✅ Upload complete!")
        print(f"\n🎉 Your model is now available at:")
        print(f"   https://huggingface.co/{REPO_NAME}")
        print(f"\n📝 Next steps:")
        print(f"   1. Update app.py to use: '{REPO_NAME}'")
        print(f"   2. Push changes to GitHub")
        print(f"   3. Redeploy on Streamlit Cloud")
        
    except Exception as e:
        print(f"\n❌ Error during upload: {e}")
        print("\n💡 Make sure you're logged in:")
        print("   Run: huggingface-cli login")
        print("   Or set HF_TOKEN environment variable")

if __name__ == "__main__":
    print("=" * 60)
    print("🤗 Hugging Face Model Upload Script")
    print("=" * 60)
    
    # Check if logged in
    try:
        api = HfApi()
        user = api.whoami()
        print(f"\n✅ Logged in as: {user['name']}")
    except Exception:
        print("\n❌ Not logged in to Hugging Face!")
        print("\n📝 Please login first:")
        print("   pip install huggingface_hub")
        print("   huggingface-cli login")
        print("\nThen run this script again.")
        exit(1)
    
    upload_model()
