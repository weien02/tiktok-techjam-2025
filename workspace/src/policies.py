import torch
from transformers import pipeline

policy_keywords = {
    "spam": [
        "buy now", "click here", "www.", "free voucher", "order now",
        "subscribe", "limited time offer", "promotion code", "get it today"
    ],
    "advertisement": [
        "check our page", "follow us", "shop now", "official website",
        "promo", "special offer", "commercial"
    ],
    "non_visitor": [
        "never been", "heard about", "not visited", "someone told me",
        "read online", "saw on internet"
    ],
    "off_topic": [
        "traffic", "parking", "travel experience", "weather",
        "location not accessible"
    ],
    "rant": [
        "hate", "ruined my day", "personal issues", "friend problems"
    ]
}

policy_scores = {"spam": -2, "advertisement": -1.5, "non_visitor": -2, "off_topic": -1, "rant": -1}


def static_analysis(review_text):
    scores = {policy: 0 for policy in policy_keywords}
    text_lower = review_text.lower()
    for policy, keywords in policy_keywords.items():
        for kw in keywords:
            if kw in text_lower:
                scores[policy] += policy_scores[policy]
    return scores

device = 0 if torch.cuda.is_available() else -1
inference_model = pipeline(
    "zero-shot-classification",
    model="gtfintechlab/SubjECTiveQA-RELEVANT",
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
    
    # Check policy violation
    policy_result = {}
    if top_relevance_label == "irrelevant":
        
        policy_result_raw = inference_model(
            input_text,
            candidate_labels=list(policy_keywords.keys()),
            hypothesis_template="This review is an example of {}."
        )
        
        policy_result = {label: -score for label, score in zip(policy_result_raw["labels"], policy_result_raw["scores"])}
    
    return top_relevance_label, relevance_confidence, policy_result

def final_decision(static_scores, inference_scores, thresholds=None):
    if thresholds is None:
        thresholds = {policy: -0.5 for policy in policy_keywords}
    final_flags = {}
    for policy in static_scores.keys():
        combined_score = static_scores[policy] + inference_scores.get(policy, 0)
        final_flags[policy] = combined_score < thresholds[policy]  # True = violation
    violated = [policy for policy, flag in final_flags.items() if flag]
    return violated if violated else ["relevant"]

def score_review(review_text, business_description):
    # static analysis
    static_scores = static_analysis(review_text)
    # inference
    relevance_label, relevance_conf, inference_scores = inference_analysis(review_text, business_description)
    # final result
    violations = final_decision(static_scores, inference_scores)
    
    return {
        "review_text": review_text,
        "business_description": business_description,
        "relevance": relevance_label,
        "relevance_confidence": relevance_conf,
        "violations": violations,
        "static_scores": static_scores,
        "inference_scores": inference_scores
    }

reviews = [
    {
        "review_text": "Buy cheap watches at www.spam.com! Never been there but heard it's good.",
        "business_description": "Italian restaurant serving pizza and pasta."
    },
    {
        "review_text": "The pasta was delicious and service was excellent.",
        "business_description": "Italian restaurant serving pizza and pasta."
    }
]

for r in reviews:
    result = score_review(r["review_text"], r["business_description"])
    print(result)
