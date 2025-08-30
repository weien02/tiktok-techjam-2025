import os
import pandas as pd


def load_data(num_rows=5):
    base_path = os.path.join(os.path.dirname(__file__), "../../data/validation/data")
    csv_path = os.path.join(base_path, "unlabelled_reviews_data.csv")

    print(f"Loading data from {csv_path}...")

    df = pd.read_csv(csv_path)

    print("Table Headings:")
    print(df.columns.tolist())

    print(f"\nFirst {num_rows} rows:")
    print(df.head(num_rows))


if __name__ == "__main__":
    load_data()
