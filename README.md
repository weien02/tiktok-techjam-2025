# Google Location Reviews Filtering and Classification

## Project Overview

This project focuses on detecting **relevant** vs **irrelevant** Google location reviews, particularly those originating from the **Utah** region of the dataset provided by [McAuley Lab – Google Local Reviews](https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/).

Our goal was to develop a lightweight, scalable approach to identifying location-relevant reviews and filtering out spam, advertisements, off-topic content, and policy-violating entries using a mix of manual annotation, feature heuristics, and NLP classification.

---

## 1. Data Exploration & Manual Labeling

- We began by sampling **200 reviews** from the Utah dataset.
> This annotation served as the **ground truth** for evaluating automated filtering techniques.

---

## 2. Preprocessing & Feature Engineering

To ensure clean and structured input, we applied the following steps:

- **Text Cleaning**:
  - Removed HTML tags, special characters, and duplicates.
- **Metadata Retention**:
  - Preserved timestamps and `gmap_id` to enrich context.
- **User Behavior Analysis**:
  - Retrieved up to **20 additional reviews per user** from the labeled set to detect suspicious review patterns (e.g., copy-pasting, excessive promotion).
- **Business Metadata Integration**:
  - Mapped `gmap_id` to business attributes (e.g., category, description) to align review content with business type.
- **Keyword Heuristics**:
  - Identified indicative terms such as "promo code", "CEO of", or "DM for info" to flag potentially irrelevant content.

---

## 3. Review Classification Pipeline

We employed a **hybrid pipeline** combining traditional string matching with semantic classification to automate review filtering:

- **Cosine Similarity**:
  - Compared the semantic similarity between the review and the business description using embedding-based techniques.
- **Basic Heuristics**:
  - Flagged overly short reviews using string length thresholds.
- **Zero-Shot Classification via LLM**:
  - Used a pre-trained model from Hugging Face:
    ```python
    from transformers import pipeline

    inference_model = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=device,
    )
    ```
  - The model was asked to classify reviews as **["spam", "advertisement", "fake review", "rant", "genuine"]** based on the predefined criteria.

---

## 4. Iterative Refinement

Based on the classification results, we refined the approach:

- Adjusted **similarity thresholds** and **string length filters**.
- Modified LLM prompts to reduce ambiguity and false positives.
- Added more labeled examples and **pseudo-labeled reviews** to improve evaluation and confidence.


---

## 5. Scaling to the Full Dataset

While the pipeline was designed for large-scale inference, we were unable to apply it to the entire Utah dataset due to time constraints.

> Future work includes:
- Running the pipeline across the full dataset.
- Automating feedback loops using active learning.
- Building an interface to review flagged outputs.

---
