import torch
from transformers import pipeline
from .config import policy_keywords

device = 0 if torch.cuda.is_available() else -1

# Initialize pipeline once
inference_model = pipeline(
    "zero-shot-classification",
    # model="gtfintechlab/SubjECTiveQA-RELEVANT",
    model="facebook/bart-large-mnli",
    device=device
)

def inference_analysis(review_text, business_description):
    input_text = f"Business: {business_description}\nReview: {review_text}"

    # Check relevance
    relevance_result = inference_model(
        input_text,
        candidate_labels=["relevant", "irrelevant"],
        hypothesis_template="This review is {}."
    )
    top_relevance_label = relevance_result["labels"][0]
    relevance_confidence = relevance_result["scores"][0]

    # Check policy violation if irrelevant
    policy_result = {}
    if top_relevance_label == "irrelevant":
        policy_result_raw = inference_model(
            input_text,
            candidate_labels=list(policy_keywords.keys()),
            hypothesis_template="This review is an example of {}."
        )
        policy_result = {
            label: -score for label, score in zip(policy_result_raw["labels"], policy_result_raw["scores"])
        }

    return top_relevance_label, relevance_confidence, policy_result