from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Define the label mapping (update this based on your model's training)
label_mapping = {
    'LABEL_0': 'negative',
    'LABEL_1': 'positive'
}

# Load the tokenizer and model
model_path="D:\\AI_Models\\kk08\\CryptoBERT\\kk08/CryptoBERT"
tokenizer = AutoTokenizer.from_pretrained("kk08/CryptoBERT")
model = AutoModelForSequenceClassification.from_pretrained("kk08/CryptoBERT")

# Set up a sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Test it on some crypto text
result = sentiment_pipeline("Ethereum is facing a massive crash.")

# Map the label
for r in result:
    r['label'] = label_mapping.get(r['label'], r['label'])  # Map the label to a meaningful name

print(result)
