# Module 10 — Dictionaries & Files
**~7 min · Python Fundamentals**

---

## Script

**Host:**
Two more essential building blocks: **dictionaries** for structured data, and **files** for persistence.

### Dictionaries

A dictionary stores key-value pairs:

```python
model = {
    "name": "llama3",
    "size": "8B",
    "context_length": 8192,
    "is_free": True,
}

print(model["name"])               # llama3
print(model.get("author", "N/A"))  # N/A — safe access with default
```

#### Adding, Updating, Deleting

```python
model["quantization"] = "Q4_K_M"   # add new key
model["size"] = "8.03B"            # update existing key
del model["is_free"]               # remove a key

print(model)
```

#### Iterating Over a Dictionary

```python
for key, value in model.items():
    print(f"{key}: {value}")

print(list(model.keys()))
print(list(model.values()))
```

#### Nested Dictionaries

```python
catalog = {
    "llama3":  {"size": "8B",  "language": "English"},
    "mistral": {"size": "7B",  "language": "Multi"},
    "phi3":    {"size": "3.8B","language": "English"},
}

print(catalog["mistral"]["language"])  # Multi
```

---

### Files

#### Writing

```python
with open("notes.txt", "w") as f:
    f.write("My AI course notes\n")
    f.write("Dictionaries are key-value stores.\n")
```

#### Reading

```python
with open("notes.txt", "r") as f:
    content = f.read()
    print(content)

# Line by line
with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())
```

#### Appending (without overwriting)

```python
with open("notes.txt", "a") as f:
    f.write("Files are great for persistence.\n")
```

Always use the `with` statement — it automatically closes the file even if an error occurs.

#### JSON Files

JSON is the universal data format for AI APIs:

```python
import json

data = {"model": "llama3", "tokens": 1024}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

with open("data.json", "r") as f:
    loaded = json.load(f)
    print(loaded["model"])
```

---

## Practice

Write `model_catalog.py` that saves the model catalog dictionary to `catalog.json`, then reads it back and prints each model's name and size.
