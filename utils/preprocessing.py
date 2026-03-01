import pandas as pd
import re
import nltk

# download stopwords
nltk.download('stopwords')

from nltk.corpus import stopwords

# load stopwords
stop_words = set(stopwords.words('english'))

# text cleaning function
def clean_text(text):

    # convert to lowercase
    text = text.lower()

    # remove URLs
    text = re.sub(r'http\S+', '', text)

    # remove mentions (@user)
    text = re.sub(r'@\w+', '', text)

    # remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # remove stopwords
    words = text.split()

    words = [word for word in words if word not in stop_words]

    # join words
    text = " ".join(words)

    return text


# load dataset
data = pd.read_csv("data/train.csv")

# apply cleaning
data["clean_text"] = data["comment_text"].astype(str).apply(clean_text)

# create label column
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


data["label"] = data.apply(create_label, axis=1)

# keep only needed columns
data = data[["clean_text", "label"]]

# save processed dataset
data.to_csv("data/processed_train.csv", index=False)

print("Preprocessing completed")
print(data.head())
