# Module 03 — Strings & F-Strings
**~6 min · Python Fundamentals**

---

## Script

**Host:**
Strings — pieces of text — are everywhere in AI work: prompts, responses, file contents. Let's master them.

### Creating Strings

```python
single  = 'Hello'
double  = "World"
multi   = """This string
spans multiple
lines."""
```

Single and double quotes work the same way. Use triple quotes for multi-line strings.

### Common String Operations

```python
greeting = "hello world"

print(len(greeting))          # 11 — number of characters
print(greeting.upper())       # HELLO WORLD
print(greeting.title())       # Hello World
print(greeting.replace("world", "Python"))  # hello Python
print(greeting.split(" "))    # ['hello', 'world']
print("  spaces  ".strip())   # 'spaces' — removes leading/trailing whitespace
```

### Concatenation

```python
first = "Hello"
second = "World"
combined = first + " " + second
print(combined)   # Hello World
```

### F-Strings (Modern Python — Use These!)

F-strings let you embed variables directly inside a string:

```python
name = "Alice"
age  = 30

print(f"My name is {name} and I am {age} years old.")
print(f"Next year I will be {age + 1}.")
print(f"Name has {len(name)} letters.")
```

The `f` before the quote activates the f-string. Anything inside `{}` is evaluated as Python code.

### Checking String Contents

```python
sentence = "Python is great for AI"

print("Python"  in sentence)   # True
print("Java"    in sentence)   # False
print(sentence.startswith("Python"))   # True
print(sentence.endswith("AI"))         # True
```

---

## Practice

Create `strings.py` that asks for the user's name with `input()`, then prints a personalised greeting using an f-string.
