# Module 02 — Variables & Data Types
**~6 min · Python Fundamentals**

---

## Script

**Host:**
Programs need to remember information. We store information in **variables**.

```python
name = "Alice"
```

That's it. No `var`, no `let`, no type declaration — Python figures it out. The `=` sign is the **assignment operator**: it puts the value on the right into the variable on the left.

### The Four Basic Types

```python
name        = "Alice"    # str  — text, always in quotes
age         = 30         # int  — whole number
temperature = 98.6       # float — decimal number
is_learning = True       # bool — True or False (capital T/F!)
```

You can check what type a variable is:

```python
print(type(name))         # <class 'str'>
print(type(age))          # <class 'int'>
print(type(temperature))  # <class 'float'>
print(type(is_learning))  # <class 'bool'>
```

### Changing Variables

Variables can be updated at any time:

```python
score = 0
print(score)   # 0

score = 10
print(score)   # 10

score = score + 5
print(score)   # 15
```

### Naming Rules

- Use lowercase letters and underscores: `my_variable`
- Can't start with a number: `1variable` ❌
- Case-sensitive: `Name` and `name` are different variables

---

## Practice

Create `variables.py` with at least one variable of each type and print them all.
