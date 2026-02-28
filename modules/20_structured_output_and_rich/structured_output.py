# structured_output.py — Module 20 (Part A)
"""
Extract structured JSON data from an LLM using Ollama's format="json".

Requirements:
    pip install ollama
    ollama pull llama3.2
"""

import json
import ollama

MODEL = "llama3.2"


def extract_product_info(review: str) -> dict:
    """Extract structured product info from a review."""
    prompt = (
        "Extract information from the following product review.\n"
        "Return ONLY valid JSON with these keys:\n"
        "  product_name (string), rating (integer 1-5),\n"
        "  pros (list of strings), cons (list of strings),\n"
        "  would_recommend (boolean)\n\n"
        f'Review: "{review}"\nJSON:'
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    return json.loads(response["message"]["content"])


def is_valid(data: dict) -> bool:
    """Basic schema validation."""
    required = {"product_name", "rating", "pros", "cons", "would_recommend"}
    return (
        required.issubset(data.keys())
        and isinstance(data["rating"], int)
        and 1 <= data["rating"] <= 5
        and isinstance(data["pros"], list)
        and isinstance(data["cons"], list)
    )


SAMPLE_REVIEW = (
    "I've been using the TechBook Pro for three months. "
    "The battery lasts 12 hours easily and the keyboard is great to type on. "
    "The webcam quality is poor and the fan gets loud under load. "
    "I'd still recommend it to anyone who values battery life."
)

if __name__ == "__main__":
    info = extract_product_info(SAMPLE_REVIEW)
    print("Extracted data:")
    print(json.dumps(info, indent=2))
    print()
    print("Valid?", "✅ Yes" if is_valid(info) else "❌ No — unexpected structure")
