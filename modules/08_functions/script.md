# Module 08 — Functions
**~7 min · Python Fundamentals**

---

## Script

**Host:**
Functions let you write a block of code once and reuse it as many times as you like. They are the single most important concept for writing clean, maintainable programs.

### Defining and Calling a Function

```python
def say_hello():
    print("Hello!")

say_hello()   # call it
say_hello()   # call it again — same code, no repetition
```

### Parameters and Return Values

```python
def add(a, b):
    result = a + b
    return result

total = add(3, 4)
print(total)   # 7
```

`return` sends a value back to the caller. After `return`, the function stops.

### Default Parameter Values

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))             # Hello, Alice!
print(greet("Bob", "Good morning"))  # Good morning, Bob!
```

### Keyword Arguments

```python
def describe_model(name, size, quantization="Q4"):
    print(f"{name} | {size} | {quantization}")

describe_model("llama3", "8B")
describe_model(name="mistral", size="7B", quantization="Q8")
describe_model("phi3", quantization="Q4", size="3B")  # order doesn't matter with keywords
```

### Docstrings

Always add a short description right inside the function:

```python
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32

print(celsius_to_fahrenheit(100))   # 212.0
```

### Scope — Variables Inside Functions

Variables created inside a function only exist inside that function:

```python
def my_function():
    x = 10   # local variable
    print(x)

my_function()
# print(x)   # This would raise a NameError — x doesn't exist here
```

---

## Practice

Write `functions_practice.py` with a function `is_palindrome(word)` that returns `True` if the word reads the same forwards and backwards (e.g. "racecar"), and `False` otherwise.
