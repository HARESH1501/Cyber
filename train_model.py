import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizer
from transformers import DistilBertForSequenceClassification
from transformers import Trainer, TrainingArguments

# Load processed dataset
data = pd.read_csv("data/processed_train.csv")

# Remove empty rows
data = data.dropna()

# Convert columns to list
texts = data["clean_text"].astype(str).tolist()
labels = data["label"].astype(int).tolist()

# Split dataset into training and validation
train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42
)

# Load tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Tokenize texts
train_encodings = tokenizer(
    train_texts,
    truncation=True,
    padding=True,
    max_length=128
)

val_encodings = tokenizer(
    val_texts,
    truncation=True,
    padding=True,
    max_length=128
)

# Create custom dataset class
class CyberDataset(torch.utils.data.Dataset):

    def __init__(self, encodings, labels):

        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):

        item = {}

        for key in self.encodings:
            item[key] = torch.tensor(self.encodings[key][idx])

        item["labels"] = torch.tensor(self.labels[idx])

        return item

    def __len__(self):

        return len(self.labels)


# Create dataset objects
train_dataset = CyberDataset(train_encodings, train_labels)
val_dataset = CyberDataset(val_encodings, val_labels)

# Load DistilBERT model
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=6
)

# Training arguments (UPDATED FOR TRANSFORMERS 5.x)
training_args = TrainingArguments(

    output_dir="./results",

    num_train_epochs=1,

    per_device_train_batch_size=8,

    per_device_eval_batch_size=8,

    eval_strategy="epoch",

    save_strategy="epoch",

    logging_dir="./logs",

    logging_steps=100,

    load_best_model_at_end=False,

    report_to="none"
)

# Create Trainer
trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=val_dataset,

)

# Start training
trainer.train()

# Save model and tokenizer
model.save_pretrained("model")
tokenizer.save_pretrained("model")

print("\nTraining completed successfully!")
print("Model saved in 'model/' folder")
