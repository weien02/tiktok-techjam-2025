import torch
from transformers import pipeline
from .config import policy_keywords

device = 0 if torch.cuda.is_available() else -1

# Initialize pipeline once
inference_model = pipeline(
    "zero-shot-classification",
    # model="gtfintechlab/SubjECTiveQA-RELEVANT",
    model="facebook/bart-large-mnli",
    device=device,
)


def inference_analysis(review_text, business_description, threshold=0.6):
    print(review_text)
    print(business_description)

    input_text = (
        f"Business Description: {business_description}\nUser Review: {review_text}"
    )

    # Reframed labels for more targeted classification
    behavior_labels = ["spam", "advertisement", "fake review", "rant", "genuine"]

    classification = inference_model(
        input_text,
        candidate_labels=behavior_labels,
        hypothesis_template="This review is {}.",
        multi_label=True,
    )

    # Filter labels by threshold
    filtered_labels = [
        (label, score)
        for label, score in zip(classification["labels"], classification["scores"])
        if score >= threshold
    ]

    return {
        "filtered_labels": [label for label, _ in filtered_labels],
        "filtered_scores": {label: score for label, score in filtered_labels},
        "all_scores": dict(zip(classification["labels"], classification["scores"])),
    }
