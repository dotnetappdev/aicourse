# Module 09 — Lists
**~6 min · Python Fundamentals**

---

## Script

**Host:**
A **list** holds multiple values in order. It's one of Python's most-used data structures — especially in AI, where you'll store message histories, retrieved chunks, and model responses as lists.

### Creating and Accessing Lists

```python
models = ["llama3", "mistral", "phi3", "gemma"]

print(models[0])    # llama3  — first item (index 0)
print(models[-1])   # gemma   — last item
print(models[1:3])  # ['mistral', 'phi3']  — slice
print(len(models))  # 4
```

### Modifying Lists

```python
models.append("qwen2")          # add to end
models.insert(1, "codellama")   # insert at index 1
models.remove("phi3")           # remove by value
popped = models.pop()           # remove & return last item
print(popped)

models[0] = "llama3.2"          # update by index
```

### Useful List Methods

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

numbers.sort()
print(numbers)          # [1, 1, 2, 3, 4, 5, 6, 9]

numbers.reverse()
print(numbers)          # [9, 6, 5, 4, 3, 2, 1, 1]

print(numbers.count(1)) # 2 — how many times 1 appears
print(numbers.index(5)) # 2 — index of first occurrence of 5
```

### List Comprehensions

Create a new list by transforming another:

```python
names   = ["alice", "bob", "charlie"]
upper   = [name.upper() for name in names]
long    = [name for name in names if len(name) > 4]

print(upper)   # ['ALICE', 'BOB', 'CHARLIE']
print(long)    # ['charlie']
```

### Checking Membership

```python
if "mistral" in models:
    print("Mistral is available")
```

---

## Practice

Write `list_practice.py` that starts with a list of 5 numbers, removes any number over 50, sorts the remaining numbers, and prints the result.
