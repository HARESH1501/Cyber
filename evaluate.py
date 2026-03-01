import torch
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Download stopwords
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# Clean text function (same as training)
def clean_text(text):

    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)

# Create label function (same as training)
def create_label(row):

    if row['threat'] == 1:
        return 5
    elif row['identity_hate'] == 1:
        return 4
    elif row['severe_toxic'] == 1:
        return 3
    elif row['obscene'] == 1:
        return 2
    elif row['insult'] == 1:
        return 1
    elif row['toxic'] == 1:
        return 1
    else:
        return 0

# Load dataset
data = pd.read_csv("data/train.csv", engine="python", on_bad_lines="skip")

print("Dataset loaded:", data.shape)

# Apply preprocessing
data["clean_text"] = data["comment_text"].astype(str).apply(clean_text)

# Apply label creation
data["label"] = data.apply(create_label, axis=1)

# BALANCED validation dataset (IMPORTANT FIX)
val_data = data.groupby("label", group_keys=False).apply(
    lambda x: x.sample(500, replace=True, random_state=42)
)

print("\nBalanced validation samples per class:")
print(val_data["label"].value_counts())

# Load model
model_path = "data/cyberbullying_model_balanced"

model = DistilBertForSequenceClassification.from_pretrained(model_path)
tokenizer = DistilBertTokenizer.from_pretrained(model_path, local_files_only=True)

model.eval()

texts = val_data["clean_text"].tolist()
true_labels = val_data["label"].tolist()

predictions = []

print("\nRunning evaluation...")

# Prediction loop
for text in texts:

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    pred = torch.argmax(outputs.logits).item()

    predictions.append(pred)

# Calculate accuracy
accuracy = accuracy_score(true_labels, predictions)

print("\n==============================")
print("FINAL MODEL EVALUATION")
print("==============================")

print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(true_labels, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(true_labels, predictions))

print("\nEvaluation completed successfully.")
