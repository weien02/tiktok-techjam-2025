import pandas as pd

reviews_df = pd.read_excel(r"workspace\data\validation\raw_data\reviews.xlsx")
restaurants_df = pd.read_excel(r"workspace\data\validation\raw_data\restaurants.xlsx")

merged_df = pd.merge(reviews_df, restaurants_df, on="URL", how="inner")

merged_df.to_csv(r"workspace\data\validation\data\unlabelled_reviews_data.csv", index=False, encoding="utf-8")

print("Saved.")
