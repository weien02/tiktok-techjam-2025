import re
from .config import policy_keywords, policy_scores
from sentence_transformers import SentenceTransformer, util

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Precompute keyword embeddings
policy_embeddings = {
    policy: embedding_model.encode(keywords, convert_to_tensor=True)
    for policy, keywords in policy_keywords.items()
}

# Dynamic thresholds per policy (tunable)
policy_thresholds = {
    "spam": 0.27,
    "advertisement": 0.27,
    "non_visitor": 0.27,
    "off_topic": 0.27,
}


def length_penalty(review_text, min_length=5, penalty=-0.1):
    """
    Penalize reviews shorter than min_length words.

    Args:
        review_text (str): The review text.
        min_length (int): Minimum acceptable number of words.
        penalty (float): Penalty score to apply if review is too short.

    Returns:
        float: Penalty score (0 if review length is sufficient).
    """
    if not review_text:
        return penalty

    length = len(review_text.strip().split())
    if length < min_length:
        return penalty
    return 0.0


def static_analysis(review_text, top_k=3):
    """
    Enhanced static analysis combining:
    - Exact keyword match
    - Semantic similarity (Top-K + Max)
    - Short-text / URL / ALL-CAPS boosting
    - Per-policy dynamic thresholds
    """
    if not review_text:
        review_text = "No review provided"
    text = review_text.strip()
    text_lower = text.lower()
    length = len(text.split())

    scores = {policy: 0 for policy in policy_keywords}
    flagged_exact = set()

    # --- Exact keyword match ---
    for policy, keywords in policy_keywords.items():
        for kw in keywords:
            if kw in text_lower:
                scores[policy] += policy_scores[policy]
                flagged_exact.add(policy)

    # --- Semantic similarity ---
    review_embedding = embedding_model.encode(text, convert_to_tensor=True)
    for policy, keyword_embeds in policy_embeddings.items():
        # Skip semantic boost if exact match already found
        if policy in flagged_exact:
            continue

        similarities = util.cos_sim(review_embedding, keyword_embeds).squeeze(0)
        top_k_vals = similarities.topk(min(top_k, len(similarities))).values
        top_k_mean = top_k_vals.mean().item()
        max_sim = similarities.max().item()

        # Weighted combination
        effective_sim = 0.5 * max_sim + 0.5 * top_k_mean

        # Adjust threshold slightly for very short or very long reviews
        threshold = policy_thresholds.get(policy, 0.3)
        if length < 8:
            threshold *= 0.7
        elif length > 30:
            threshold *= 1.2

        if effective_sim >= threshold:
            scores[policy] += policy_scores[policy] * effective_sim  # weighted score

    # --- Boost for URLs or ALL-CAPS ---
    if re.search(r"http\S+|www\.\S+", text_lower) or text.isupper():
        if "spam" in scores:
            scores["spam"] += abs(policy_scores.get("spam", 0)) * 0.7  # partial boost

    # --- Ensure minimum policy score ---
    for policy in scores:
        if scores[policy] < policy_scores.get(policy, 0):
            scores[policy] = policy_scores[policy]

    return scores
