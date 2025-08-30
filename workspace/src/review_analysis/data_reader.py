import os
import pandas as pd


def load_data():
    base_path = os.path.join(os.path.dirname(__file__), "../..", "data", "raw")
    review_path = os.path.join(base_path, "review-Alabama.json")
    meta_path = os.path.join(base_path, "meta-Alabama.json")

    print("Starting to load review data...")
    reviews_df = pd.read_json(review_path, lines=True)
    print(f"Loaded {len(reviews_df)} review rows.")

    print("Starting to load meta data...")
    meta_df = pd.read_json(meta_path, lines=True)
    print(f"Loaded {len(meta_df)} meta rows.")

    gmap_to_desc = pd.Series(
        meta_df["description"].values, index=meta_df["gmap_id"]
    ).to_dict()

    data_tuples = []
    for _, row in reviews_df.iterrows():
        review_text = row.get("text", "")
        gmap_id = row.get("gmap_id", None)

        description = gmap_to_desc.get(gmap_id, "")

        data_tuples.append((review_text, description))

    return data_tuples


if __name__ == "__main__":
    tuples = load_data()
    for review_text, desc in tuples[:5]:
        print(f"Review: {review_text[:50]}... \nDescription: {desc[:50]}...\n")
