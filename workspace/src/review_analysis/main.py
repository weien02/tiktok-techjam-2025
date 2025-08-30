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
        {
            "review_text": "I was not there actually.",
            "business_description": "Local art gallery in the city center.",
        },
        {
            "review_text": "WHY DID THEY DO THIS TO ME!!!",
            "business_description": "Tech startup specializing in AI solutions.",
        },
        {
            "review_text": "The sun was very bright.",
            "business_description": "Beachside resort with spa and dining options.",
        },
        {
            "review_text": "This deal is too good to miss! Everyone should grab one.",
            "business_description": "Electronics store in downtown."
        },
        {
            "review_text": "Exclusive savings available today on all products!",
            "business_description": "Online fashion retailer."
        },
        {
            "review_text": "Discover our newest collection online, highly recommended!",
            "business_description": "Home decor startup."
        },
        {
            "review_text": "Visit our brand for special goodies this season.",
            "business_description": "Tech gadget company."
        },
        {
            "review_text": "A friend told me this place has the best sushi.",
            "business_description": "Japanese restaurant."
        },
        {
            "review_text": "People say the gallery is worth a visit, I haven’t seen it myself.",
            "business_description": "Local art gallery."
        },
        {
            "review_text": "The construction around the area is a nightmare.",
            "business_description": "Cafe near city center."
        },
        {
            "review_text": "The neighborhood is noisy and chaotic at night.",
            "business_description": "Hotel with spa services."
        },
        {
            "review_text": "Completely frustrated with how they handled my order!",
            "business_description": "Local bakery."
        },
        {
            "review_text": "Everything went wrong today, can’t believe this service.",
            "business_description": "Electronics store."
        }
    ]

    for r in sample_reviews:
        result = score_review(r["review_text"], r["business_description"])
        print(result)


if __name__ == "__main__":
    main()
