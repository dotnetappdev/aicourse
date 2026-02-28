# Module 05 — Conditionals (if / elif / else)
**~6 min · Python Fundamentals**

---

## Script

**Host:**
Programs make decisions. In Python, we use `if` statements to say "do this *if* some condition is true."

### Basic if / else

```python
temperature = 25

if temperature > 30:
    print("It's hot — wear a t-shirt!")
else:
    print("It's comfortable — a light jacket works.")
```

The indentation (4 spaces) is **not optional** — Python uses it to know what belongs inside the `if`.

### if / elif / else

Use `elif` ("else if") to check multiple conditions:

```python
score = 72

if score >= 90:
    print("A — Excellent!")
elif score >= 80:
    print("B — Great job!")
elif score >= 70:
    print("C — Good effort!")
elif score >= 60:
    print("D — Needs improvement.")
else:
    print("F — Please see your instructor.")
```

Python checks each condition in order and stops at the **first True one**.

### Comparison Operators

```python
x = 10
print(x == 10)   # True   — equal to
print(x != 5)    # True   — not equal to
print(x > 8)     # True   — greater than
print(x < 8)     # False  — less than
print(x >= 10)   # True   — greater than or equal
print(x <= 9)    # False  — less than or equal
```

### Logical Operators

Combine conditions with `and`, `or`, `not`:

```python
age  = 25
city = "New York"

if age >= 18 and city == "New York":
    print("Eligible for the local program.")

if age < 13 or age > 65:
    print("Special pricing applies.")

if not age < 18:
    print("You are an adult.")
```

### One-Line Conditional (Ternary)

```python
status = "adult" if age >= 18 else "minor"
print(status)
```

---

## Practice

Write `grade_checker.py` that asks for a score and prints the letter grade plus an encouraging message.
