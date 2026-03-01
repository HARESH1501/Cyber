from transformers import DistilBertTokenizer

# Load original DistilBERT tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Save vocab.txt into your model folder
tokenizer.save_pretrained("data/cyberbullying_model_balanced")

print("vocab.txt created successfully!")
