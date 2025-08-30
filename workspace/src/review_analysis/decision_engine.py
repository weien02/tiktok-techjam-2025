from .config import policy_keywords


def final_decision(static_scores, inference_scores, thresholds=None):
    if thresholds is None:
        thresholds = {policy: -0.3 for policy in policy_keywords}

    final_flags = {}
    for policy in static_scores.keys():
        combined_score = static_scores[policy] + inference_scores.get(policy, 0)
        final_flags[policy] = combined_score < thresholds[policy]  # True = violation

    violated = [policy for policy, flag in final_flags.items() if flag]
    return violated if violated else ["relevant"]
