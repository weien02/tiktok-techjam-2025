from .config import policy_keywords, policy_scores

def static_analysis(review_text):
    scores = {policy: 0 for policy in policy_keywords}
    text_lower = review_text.lower()
    for policy, keywords in policy_keywords.items():
        for kw in keywords:
            if kw in text_lower:
                scores[policy] += policy_scores[policy]
    return scores