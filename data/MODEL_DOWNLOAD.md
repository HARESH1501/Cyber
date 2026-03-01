# Model Files

The trained model files are too large to store on GitHub (255 MB).

## Required Files

You need to place the following files in `data/cyberbullying_model_balanced/`:

- `model.safetensors` (255 MB) - The trained DistilBERT model weights
- `config.json` - Model configuration (included)
- `tokenizer.json` - Tokenizer configuration (included)
- `tokenizer_config.json` - Tokenizer settings (included)
- `vocab.txt` - Vocabulary file (included)

## Training Data

The following CSV files are also excluded due to size:
- `data/train.csv` (65 MB)
- `data/test.csv` (57 MB)
- `data/processed_train.csv`

## How to Get the Model

1. Train the model yourself using `train_model.py`
2. Or download from your cloud storage/drive
3. Place the files in the correct directories as shown above

## Model Information

- **Model**: DistilBERT for Sequence Classification
- **Accuracy**: 91.30%
- **Categories**: 6 (Normal, Toxic, Obscene, Severe Toxic, Hate Speech, Threat)
- **Framework**: PyTorch + Transformers
