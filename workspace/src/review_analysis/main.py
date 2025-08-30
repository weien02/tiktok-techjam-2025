from review_analysis.static_analysis import static_analysis
from review_analysis.inference_analysis import inference_analysis
from review_analysis.decision_engine import final_decision

import pandas as pd
import os

from review_analysis.data_reader import (
    load_jsonl_data,
)


def score_review(merged_df):
    # Get the first row
    first_row = merged_df.iloc[1]
    review_text = first_row.get("review", "No review provided")
    description = first_row.get("description", "No description")
    category = first_row.get("category", [])
    business_details = {"description": description, "category": category}

    # Call inference_analysis
    result = inference_analysis(review_text, business_details)

    print("Inference result:")
    print(result)


def main():
    base_path = os.path.join(os.path.dirname(__file__), "../../sampleData/")
    user_reviews_file = os.path.join(base_path, "user_past_reviews.jsonl")
    gmap_locations_file = os.path.join(base_path, "unique_gmap_ids.jsonl")

    user_reviews_df, gmap_locations_df = load_jsonl_data(
        user_reviews_file, gmap_locations_file
    )
    merged_df = pd.merge(user_reviews_df, gmap_locations_df, on="gmap_id", how="inner")
    score_review(merged_df)


if __name__ == "__main__":
    main()
