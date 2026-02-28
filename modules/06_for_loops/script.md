# Module 06 — For Loops
**~6 min · Python Fundamentals**

---

## Script

**Host:**
When you need to do something repeatedly, you use a **loop**. The `for` loop is the most common — it repeats once for each item in a sequence.

### Looping Over a List

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like {fruit}")
```

The variable `fruit` takes a different value each time the loop runs.

### range()

`range()` generates a sequence of numbers — perfect when you need to repeat something N times.

```python
for i in range(5):
    print(i)   # 0, 1, 2, 3, 4

for i in range(1, 6):
    print(i)   # 1, 2, 3, 4, 5

for i in range(0, 10, 2):
    print(i)   # 0, 2, 4, 6, 8  (step of 2)
```

### enumerate() — Index + Value Together

```python
models = ["llama3", "mistral", "phi3"]

for index, model in enumerate(models):
    print(f"{index + 1}. {model}")
```

Output:
```
1. llama3
2. mistral
3. phi3
```

### Loop Control: break and continue

```python
# break — stop the loop early
for i in range(10):
    if i == 5:
        break
    print(i)   # prints 0, 1, 2, 3, 4

# continue — skip the current iteration
for i in range(5):
    if i == 2:
        continue
    print(i)   # prints 0, 1, 3, 4
```

### List Comprehension — Create a List in One Line

```python
squares     = [x ** 2 for x in range(6)]
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]

print(squares)       # [0, 1, 4, 9, 16, 25]
print(even_squares)  # [0, 4, 16, 36, 64]
```

---

## Practice

Write `loop_practice.py` that prints a multiplication table for the number 7 (7×1 through 7×10) using a `for` loop.
