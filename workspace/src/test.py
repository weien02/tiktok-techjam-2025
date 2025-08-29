import json
from transformers import pipeline

def load_reviews(file_path):
    reviews = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            review = json.loads(line)
            review_text = review.get("text", "")
            if not review_text:
                continue  # skip empty reviews
            reviews.append(review)  # each line is one JSON object
    return reviews

def main():
    # Load zero-shot classifier (DistilBERT MNLI distilled from BART)
    classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")

    # Load example reviews
    reviews = load_reviews("../data/test.json")

    # Define your labels
    labels = ["relevant", "irrelevant", "spam"]

    # Go through each review
    for entry in reviews:
        review_text = entry.get("text", "")
        if not review_text.strip():
            continue  # skip empty reviews
        
        # Run classification
        result = classifier(review_text, candidate_labels=labels)

        top_label = result['labels'][0]
        top_score = result['scores'][0]

        print("="*60)
        print(f"Review: {review_text}")
        print(f"Predicted label: {top_label} (score: {top_score:.2f})")
        print("All scores:", dict(zip(result['labels'], [round(s, 2) for s in result['scores']])))
        print("="*60)

if __name__ == "__main__":
    main()
