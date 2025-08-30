from dataclasses import dataclass, field
from typing import List, Dict


@dataclass(slots=True)
class Review:
    review_text: str
    business: str = ""
    violations: List[str] = field(default_factory=list)
    static_scores: Dict[str, int] = field(default_factory=dict)
    inference_scores: Dict[str, float] = field(default_factory=dict)
    final_verdict: bool = False
    score: int = 0

    def __str__(self) -> str:
        return (
            "Review(\n"
            f"  text={self.review_text!r},\n"
            f"  business={self.business!r},\n"
            f"  violations={self.violations},\n"
            f"  static_scores={self.static_scores},\n"
            f"  inference_scores={self.inference_scores},\n"
            f"  final_verdict={self.final_verdict}\n"
            f"  score={self.score},\n"
            ")"
        )


# -----------------------
# Example usage
# -----------------------
if __name__ == "__main__":
    r = Review(
        review_text="Buy cheap watches at www.spam.com! Never been there but heard it's good.",
        business="Watch store",
        violations=["advertisement", "not_visited"],
        static_scores={"length": 42},
        inference_scores={"bert_classifier": 0.11, "gpt_label": 0.05},
        final_verdict=False,
    )
    print(r)
