import torch
import re
import nltk
from nltk.corpus import stopwords
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):

    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)

# USE BALANCED MODEL
model_path = "data/cyberbullying_model_balanced"

model = DistilBertForSequenceClassification.from_pretrained(model_path)
tokenizer = DistilBertTokenizer.from_pretrained(model_path)

labels_map = {
    0: "Normal",
    1: "Toxic / Insult",
    2: "Obscene",
    3: "Severe Toxic",
    4: "Hate Speech",
    5: "Threat"
}

text = input("Enter text: ")

cleaned_text = clean_text(text)

inputs = tokenizer(cleaned_text, return_tensors="pt")

outputs = model(**inputs)

prediction = torch.argmax(outputs.logits).item()

print("\nCleaned text:", cleaned_text)
print("Prediction:", labels_map[prediction])
