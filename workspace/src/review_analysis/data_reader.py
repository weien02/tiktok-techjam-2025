import os
import pandas as pd


def load_csv_data(num_rows=5):
    base_path = os.path.join(os.path.dirname(__file__), "../../data/validation/data")
    csv_path = os.path.join(base_path, "unlabelled_reviews_data.csv")

    print(f"Loading data from {csv_path}...")

    df = pd.read_csv(csv_path)

    print("Table Headings:")
    print(df.columns.tolist())

    print(f"\nFirst {num_rows} rows:")
    print(df.head(num_rows))


def load_jsonl_data(user_review_path, gmap_location_path, num_rows=5):
    print(f"Loading user reviews from: {user_review_path}")
    df = pd.read_json(user_review_path, lines=True)

    print(f"Loading gmap locations from: {gmap_location_path}")
    df2 = pd.read_json(gmap_location_path, lines=True)

    print("\nUser Review Table Headings:")
    print(df.columns.tolist())

    print(f"\nFirst {num_rows} rows of user reviews:")
    print(df.head(num_rows))

    print("\nGMap Location Table Headings:")
    print(df2.columns.tolist())

    print(f"\nFirst {num_rows} rows of gmap locations:")
    print(df2.head(num_rows))
    return df, df2


def create_tuples(merged_df):
    result = []
    for _, row in merged_df.iterrows():
        review = row["review"] if pd.notna(row["review"]) else "No review provided"
        description = row["description"] if "description" in row else "No description"
        category = row["category"] if "category" in row else "No category"
        if isinstance(category, list):
            category = frozenset(category)

        result.append((review, description, category))
    result = list(set(result))
    return result


def get_reviews_grouped_by_user(merged_df):
    grouped_reviews = {}

    for _, row in merged_df.iterrows():
        user_id = row["user_id"]
        review = row["review"] if pd.notna(row["review"]) else "No review provided"

        # Optionally include additional info (like gmap_id, rating, etc.)
        review_entry = {
            "review": review,
            "gmap_id": row.get("gmap_id"),
            "description": row.get("description"),
            "category": row.get("category"),
            "rating": row.get("rating"),
        }

        if user_id not in grouped_reviews:
            grouped_reviews[user_id] = []

        grouped_reviews[user_id].append(review_entry)

    return grouped_reviews


if __name__ == "__main__":
    # Example usage with relative paths
    base_path = os.path.join(os.path.dirname(__file__), "../../sampleData/")
    user_reviews_file = os.path.join(base_path, "user_past_reviews.jsonl")
    gmap_locations_file = os.path.join(base_path, "unique_gmap_ids.jsonl")

    user_reviews_df, gmap_locations_df = load_jsonl_data(
        user_reviews_file, gmap_locations_file
    )
