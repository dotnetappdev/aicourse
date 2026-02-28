# Module 04 — Numbers & Operators
**~5 min · Python Fundamentals**

---

## Script

**Host:**
Python is a great calculator. Let's cover all the operators you'll use regularly.

### Arithmetic Operators

```python
x = 10
y = 3

print(x + y)    # 13  — addition
print(x - y)    # 7   — subtraction
print(x * y)    # 30  — multiplication
print(x / y)    # 3.333... — division (always returns float)
print(x // y)   # 3   — floor division (drops the decimal)
print(x % y)    # 1   — modulus (remainder)
print(x ** y)   # 1000 — exponentiation (10³)
```

The modulus operator `%` is handy for checking if a number is even or odd:

```python
number = 7
if number % 2 == 0:
    print("Even")
else:
    print("Odd")
```

### Shorthand Assignment

```python
score = 100
score += 10   # same as: score = score + 10
score -= 5    # same as: score = score - 5
score *= 2    # same as: score = score * 2
score //= 3   # same as: score = score // 3
print(score)
```

### int vs float

```python
print(10 / 2)    # 5.0  — always float
print(10 // 2)   # 5    — int

# Convert between types
print(int(3.9))    # 3  (truncates, does NOT round)
print(float(5))    # 5.0
print(round(3.14159, 2))  # 3.14
```

### Useful Math Functions

```python
import math

print(abs(-7))          # 7   — absolute value
print(max(3, 7, 1))     # 7
print(min(3, 7, 1))     # 1
print(sum([1, 2, 3]))   # 6
print(math.sqrt(16))    # 4.0
print(math.pi)          # 3.14159...
```

---

## Practice

Write `calculator.py` that asks the user for two numbers and prints the result of all six arithmetic operations.
