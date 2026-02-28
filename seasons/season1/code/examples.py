# Season 1 — Code Examples

# ── Episode 1: Variables & Data Types ──────────────────────────────────────

# hello.py
print("Hello, World!")

# Basic variables
name = "Alice"
age = 30
temperature = 98.6
is_learning = True

print(name)
print(age)
print(temperature)
print(is_learning)

# Math operators
x = 10
y = 3

print(x + y)    # 13
print(x - y)    # 7
print(x * y)    # 30
print(x / y)    # 3.333...
print(x // y)   # 3  (floor division)
print(x % y)    # 1  (modulus / remainder)
print(x ** y)   # 1000

# String concatenation and f-strings
first_name = "Alice"
last_name  = "Smith"
full_name  = first_name + " " + last_name
print(full_name)
print(f"Hello, {full_name}! You are {age} years old.")


# ── Episode 2: Control Flow & Functions ────────────────────────────────────

# if / elif / else
score = 85

if score >= 90:
    print("A — Excellent!")
elif score >= 80:
    print("B — Great job!")
elif score >= 70:
    print("C — Not bad.")
else:
    print("Keep practicing!")

# for loop over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")

# range-based for loop
for i in range(5):
    print(i)

# while loop
count = 0
while count < 3:
    print(f"Count is {count}")
    count += 1

# Functions
def greet(name, greeting="Hello"):
    """Return a personalised greeting string."""
    return f"{greeting}, {name}!"

print(greet("Bob"))
print(greet("Charlie", "Hi"))


# ── Episode 3: Lists, Dicts, and Files ─────────────────────────────────────

# Lists
models = ["llama3", "mistral", "phi3", "gemma"]
print(models[0])
print(models[-1])
print(len(models))

models.append("qwen2")
models.remove("phi3")

upper_models = [m.upper() for m in models]
print(upper_models)

# Dictionaries
model_info = {
    "name": "llama3",
    "parameters": "8B",
    "context_length": 8192,
    "is_free": True,
}

print(model_info["name"])
print(model_info.get("size", "unknown"))

model_info["quantization"] = "Q4_K_M"
print(model_info)

# Writing a file
with open("notes.txt", "w") as f:
    f.write("My AI course notes\n")
    f.write("Python is awesome!\n")

# Reading a file
with open("notes.txt", "r") as f:
    content = f.read()
    print(content)

# Reading line by line
with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())
