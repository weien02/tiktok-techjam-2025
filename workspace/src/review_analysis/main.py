from review_analysis.static_analysis import static_analysis, length_penalty
from review_analysis.inference_analysis import (
    inference_analysis,
    user_trustworthiness_analysis,
)
from review_analysis.decision_engine import final_decision

import pandas as pd
import os

from review_analysis.data_reader import (
    load_jsonl_data,
)
from data_conversion_script.data_conversion import Review


def apply_inference_analysis(
    merge_df,
    review_obj,
    review_text,
    business_description,
    initial_score=5.0,
    penalty_per_violation=0.2,
):
    inference_result = inference_analysis(review_text, business_description)
    inference_violations = inference_result["filtered_labels"]
    inference_scores = inference_result["filtered_scores"]

    review_obj.inference_scores = inference_scores

    filtered_violations = [v for v in inference_violations if v != "genuine"]
    is_genuine = "genuine" in inference_violations

    review_obj.violations.extend(filtered_violations)

    score = initial_score
    score -= penalty_per_violation * len(filtered_violations)
    if is_genuine:
        score += penalty_per_violation  # reward for being genuine

    return max(score, 0)


def apply_static_analysis(review_obj, review_text, threshold=0.3):
    static_scores = static_analysis(review_text)

    for policy, score in static_scores.items():
        if abs(score) >= threshold:
            if policy not in review_obj.violations:
                review_obj.violations.append(policy)
            review_obj.score += score
    penalty = length_penalty(review_text)
    if penalty < 0:
        review_obj.violations.append("short_review")
        review_obj.score += penalty

    review_obj.static_scores = static_scores


def run_review_pipeline(
    merged_df,
    max_reviews=20,
    initial_score=5,
    penalty_per_violation=1,
    final_threshold=3,
):
    all_review_objects = []

    user_groups = merged_df.groupby("user_id")

    users_processed = 0

    for user_id, user_df in user_groups:
        users_processed += 1
        if users_processed > max_reviews:
            break

        user_reviews = user_df["review"].dropna().tolist()

        user_trust_result = user_trustworthiness_analysis(user_id, user_reviews)
        is_trustworthy = "trustworthy" in user_trust_result["filtered_labels"]
        for idx, row in user_df.iterrows():
            review_text = row.get("review", "No review provided")
            description = row.get("description", "No description")
            category = row.get("category", [])
            business_description = f"{description} | Categories: {', '.join(category)}"
            if not review_text:
                review_obj = Review(
                    review_text="No review provided",
                    business=business_description,
                    violations=["no_review_text"],
                    static_scores={},
                    inference_scores={},
                    final_verdict=True,
                    score=2,
                )
                all_review_objects.append(review_obj)
                print(
                    f"\n--- Review {idx + 1} (User: {user_id}) [Skipped: No Review] ---\n{review_obj}"
                )
                continue

            review_obj = Review(
                review_text=review_text,
                business=business_description,
                violations=[],
                static_scores={},
                inference_scores={},
                final_verdict=False,
            )
            score = apply_inference_analysis(
                merged_df,
                review_obj,
                review_text,
                business_description,
                initial_score=initial_score,
                penalty_per_violation=penalty_per_violation,
            )
            review_obj.score = score

            if is_trustworthy:
                review_obj.score += 0.5
            else:
                review_obj.score -= 0.5
                review_obj.violations.append("untrustworthy_user")

            apply_static_analysis(review_obj, review_text)
            review_obj.score = max(review_obj.score, 0)
            review_obj.final_verdict = review_obj.score < final_threshold

            all_review_objects.append(review_obj)

            print(f"\n--- Review {idx + 1} (User: {user_id}) ---\n{review_obj}")

    return all_review_objects


def main():
    base_path = os.path.join(os.path.dirname(__file__), "../../sampleData/")
    user_reviews_file = os.path.join(base_path, "user_past_reviews.jsonl")
    gmap_locations_file = os.path.join(base_path, "unique_gmap_ids.jsonl")

    user_reviews_df, gmap_locations_df = load_jsonl_data(
        user_reviews_file, gmap_locations_file
    )
    merged_df = pd.merge(user_reviews_df, gmap_locations_df, on="gmap_id", how="inner")
    run_review_pipeline(merged_df)


if __name__ == "__main__":
    main()
