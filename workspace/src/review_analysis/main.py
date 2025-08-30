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


data = [
    # User 1 - spammy and advertisement reviews, off-topic
    {
        "user_id": "user1",
        "name_x": "User One",
        "review": "Buy cheap products at http://spamlink.com now!!!",
        "rating": 1,
        "time": "2025-08-01",
        "gmap_id": "loc1",
        "name_y": "Cool Cafe",
        "address": "123 Main St",
        "description": "A cozy cafe serving coffee and pastries.",
        "category": ["Cafe", "Coffee Shop"],
    },
    {
        "user_id": "user1",
        "name_x": "User One",
        "review": "Visit www.advertisehere.com for great deals on everything!",
        "rating": 1,
        "time": "2025-08-02",
        "gmap_id": "loc2",
        "name_y": "Tech Store",
        "address": "456 Market St",
        "description": "Retail store for electronics and gadgets.",
        "category": ["Electronics", "Retail"],
    },
    {
        "user_id": "user1",
        "name_x": "User One",
        "review": "This review has nothing to do with the place, just random ranting about politics.",
        "rating": 2,
        "time": "2025-08-03",
        "gmap_id": "loc3",
        "name_y": "Bookstore",
        "address": "789 Elm St",
        "description": "Local bookstore with a great selection.",
        "category": ["Bookstore", "Retail"],
    },
    # User 2 - non-visitor type review
    {
        "user_id": "user2",
        "name_x": "User Two",
        "review": "I heard this place is terrible and has bad service.",
        "rating": 1,
        "time": "2025-08-04",
        "gmap_id": "loc4",
        "name_y": "Italian Restaurant",
        "address": "321 Oak St",
        "description": "Authentic Italian cuisine with cozy atmosphere.",
        "category": ["Restaurant", "Italian"],
    },
    # User 3 - good genuine user with multiple bad reviews
    {
        "user_id": "user3",
        "name_x": "User Three",
        "review": "Spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam",
        "rating": 1,
        "time": "2025-08-05",
        "gmap_id": "loc5",
        "name_y": "Gym Center",
        "address": "654 Pine St",
        "description": "Gym with modern equipment and trainers.",
        "category": ["Gym", "Fitness"],
    },
    {
        "user_id": "user3",
        "name_x": "User Three",
        "review": "Visit www.fakeads.com now for great discounts!!!",
        "rating": 1,
        "time": "2025-08-06",
        "gmap_id": "loc6",
        "name_y": "Hair Salon",
        "address": "987 Maple Ave",
        "description": "Professional haircuts and styling.",
        "category": ["Salon", "Beauty"],
    },
    {
        "user_id": "user3",
        "name_x": "User Three",
        "review": "I never went to this place but heard they are bad.",
        "rating": 1,
        "time": "2025-08-07",
        "gmap_id": "loc7",
        "name_y": "Pet Store",
        "address": "159 Cedar Blvd",
        "description": "Pet supplies and grooming services.",
        "category": ["Pet Store", "Retail"],
    },
    {
        "user_id": "user3",
        "name_x": "User Three",
        "review": "Totally unrelated content about movies and TV shows.",
        "rating": 2,
        "time": "2025-08-08",
        "gmap_id": "loc8",
        "name_y": "Movie Theater",
        "address": "753 Birch Rd",
        "description": "Local movie theater with latest releases.",
        "category": ["Entertainment", "Cinema"],
    },
]


def main():
    base_path = os.path.join(os.path.dirname(__file__), "../../sampleData/")
    user_reviews_file = os.path.join(base_path, "user_past_reviews.jsonl")
    gmap_locations_file = os.path.join(base_path, "unique_gmap_ids.jsonl")

    user_reviews_df, gmap_locations_df = load_jsonl_data(
        user_reviews_file, gmap_locations_file
    )
    # merged_df = pd.merge(user_reviews_df, gmap_locations_df, on="gmap_id", how="inner")
    # run_review_pipeline(merged_df)
    merged_df = pd.DataFrame(data)
    print(merged_df)
    run_review_pipeline(merged_df)


if __name__ == "__main__":
    main()
