import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Define the model name you want to download
model_name = "kk08/CryptoBERT"  # Replace with your desired model

# Define the path where you want to save the model
save_directory = "D:/AI_Models/kk08/CryptoBERT"  # Replace with your desired directory

# Create the directory if it doesn't exist
os.makedirs(save_directory, exist_ok=True)

# Download and save the tokenizer and model locally
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)  # Saves tokenizer files to the directory

model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.save_pretrained(save_directory)  # Saves model files to the directory
