from review_analysis.static_analysis import static_analysis
from review_analysis.inference_analysis import inference_analysis
from review_analysis.decision_engine import final_decision

import pandas as pd
import os


def score_review(review_text, business_description):
    static_scores = static_analysis(review_text)
    relevance_label, relevance_conf, inference_scores = inference_analysis(
        review_text, business_description
    )
    violations = final_decision(static_scores, inference_scores)

    return {
        "review_text": review_text,
        "business_description": business_description,
        "relevance": relevance_label,
        "relevance_confidence": relevance_conf,
        "violations": violations,
        "static_scores": static_scores,
        "inference_scores": inference_scores,
    }


def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    json_path = os.path.join(project_root, "data", "sample_data.json")

    df = pd.read_json(json_path, lines=True)

    reviews = df.to_dict(orient="records")

    for review in reviews:
        result = score_review(
            review_text=review["text"],
            business_description=review["business_description"],
        )
        print(result)

    sample_reviews = [
        {
            "review_text": "Buy cheap watches at www.spam.com! Never been there but heard it's good.",
            "business_description": "Italian restaurant serving pizza and pasta.",
        },
        {
            "review_text": "The pasta was delicious and service was excellent.",
            "business_description": "Italian restaurant serving pizza and pasta.",
        },
    ]

    for r in sample_reviews:
        result = score_review(r["review_text"], r["business_description"])
        print(result)


if __name__ == "__main__":
    main()
