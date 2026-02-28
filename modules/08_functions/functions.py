# functions.py — Module 08

# Basic function
def say_hello():
    print("Hello!")

say_hello()
say_hello()

# Parameters and return value
def add(a, b):
    return a + b

total = add(3, 4)
print(total)

# Default parameters
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))
print(greet("Bob", "Good morning"))

# Keyword arguments
def describe_model(name, size, quantization="Q4"):
    print(f"{name} | {size} | {quantization}")

describe_model("llama3", "8B")
describe_model(name="mistral", size="7B", quantization="Q8")
describe_model("phi3", quantization="Q4", size="3B")

# Docstring + type hints
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32

print(celsius_to_fahrenheit(100))

# Practice: palindrome checker
def is_palindrome(word: str) -> bool:
    """Return True if word reads the same forwards and backwards."""
    clean = word.lower().replace(" ", "")
    return clean == clean[::-1]

print(is_palindrome("racecar"))   # True
print(is_palindrome("hello"))     # False
print(is_palindrome("A man a plan a canal Panama"))  # True
