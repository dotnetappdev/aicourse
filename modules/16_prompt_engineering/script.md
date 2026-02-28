# Module 16 — Prompt Engineering Techniques
**~7 min · Prompt Engineering**

---

## Script

**Host:**
Writing a good prompt is a skill. Here are five techniques you'll use constantly.

### 1. Be Specific

Vague prompts get vague answers. Describe exactly what you want.

```python
# Bad
prompt = "Write code."

# Good
prompt = """Write a Python function called `word_count` that:
- Takes a string as input
- Returns a dictionary where keys are words and values are occurrence counts
- Is case-insensitive (treats 'Hello' and 'hello' as the same word)
- Ignores punctuation
Include a docstring and 2 usage examples."""
```

### 2. Few-Shot Prompting — Show, Don't Just Tell

Give examples of the input-output pairs you want:

```python
prompt = """Classify the sentiment as POSITIVE, NEGATIVE, or NEUTRAL.

Review: "The coffee was amazing!"
Sentiment: POSITIVE

Review: "Waited 20 minutes for cold soup."
Sentiment: NEGATIVE

Review: "The menu has lots of options."
Sentiment: NEUTRAL

Review: "The AI course changed my life!"
Sentiment:"""
```

The model picks up the pattern from your examples.

### 3. Chain of Thought — Ask It to Think

For reasoning tasks, tell the model to work step by step:

```python
prompt = """A store has 50 apples. They sell 3 bags of 6 apples each,
then receive a delivery of 20 apples. How many apples do they have?

Think through this step by step before giving your final answer."""
```

### 4. Specify the Output Format

Tell the model exactly what structure you want:

```python
prompt = """List the top 3 reasons to use Python for AI development.

Format your response as a numbered list where each item has:
- A bold title
- A one-sentence explanation

Example format:
1. **Title**: Explanation here.
"""
```

### 5. Assign a Role (Role Prompting)

```python
system = """You are a senior code reviewer with 15 years of Python experience.
When reviewing code, focus on:
1. Correctness and edge cases
2. Readability and naming
3. Pythonic style
4. Performance (only if it matters)

Be specific — point to line numbers or specific patterns."""
```

### Combining Techniques

The best prompts combine multiple techniques:

```python
system = "You are a Python expert. Be concise."
user   = """Review this function and suggest improvements.
Think step by step. Return your answer as JSON with keys:
"issues" (list of strings) and "improved_code" (string).

Code:
def calc(x,y):
    return x+y
"""
```

---

## Practice

Write `sentiment_classifier.py` that uses few-shot prompting to classify a list of product reviews as POSITIVE, NEGATIVE, or NEUTRAL.
