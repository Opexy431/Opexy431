import requests
from PIL import Image
from transformers import ViTForImageClassification, ViTFeatureExtractor
import torch

# Load the pre-trained model 
model_name = "google/vit-base-patch16-224"
model = ViTForImageClassification.from_pretrained(model_name)
feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)

# Load an image using Pillow
image_path = "path/to/your/image.jpg"
image = Image.open(image_path)

# Preprocess the image
inputs = feature_extractor(images=image, return_tensors="pt")

# Make predictions
with torch.no_grad():
    outputs = model(**inputs)

# Get the predicted class
logits = outputs.logits
predicted_class = logits.argmax(-1).item()

# Load the labels (if available)
labels = model.config.id2label if hasattr(model.config, 'id2label') else {i: f'Label_{i}' for i in range(model.config.num_labels)}
predicted_label = labels[predicted_class]

print(f"Predicted class index: {predicted_class}")
print(f"Predicted label: {predicted_label}")

# Query the Wikipedia API for information about the predicted label
wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={predicted_label}&prop=extracts&exintro&explaintext"

try:
    response = requests.get(wiki_url)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    data = response.json()
 
    # Parse the response
    page = next(iter(data['query']['pages'].values()))
    if 'extract' in page:
        print(f"\nWikipedia Summary for {predicted_label}:\n{page['extract']}")
    else:
        print("No information found on Wikipedia.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching information: {e}")
