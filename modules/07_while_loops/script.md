# Module 07 — While Loops
**~5 min · Python Fundamentals**

---

## Script

**Host:**
A `while` loop keeps running as long as a condition is `True`. Use it when you don't know in advance how many times you need to repeat.

### Basic While Loop

```python
count = 0

while count < 5:
    print(f"Count: {count}")
    count += 1   # IMPORTANT: always update the condition variable

print("Done!")
```

If you forget `count += 1`, the loop runs forever — called an **infinite loop**. Press **Ctrl+C** to stop one.

### User-Input Loop

The most common use of `while` in real applications: keep asking until the user gives valid input.

```python
while True:
    answer = input("Type 'yes' or 'no': ").lower()
    if answer in ("yes", "no"):
        break
    print("Invalid input, try again.")

print(f"You chose: {answer}")
```

`while True` creates an infinite loop on purpose — we exit it with `break` once we're satisfied.

### Countdown Example

```python
countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
print("Liftoff!")
```

### for vs while — Which to Use?

| Situation | Use |
|-----------|-----|
| Known number of iterations | `for` |
| Loop over a collection | `for` |
| Unknown iterations, condition-based | `while` |
| Keep asking until valid input | `while True` + `break` |

---

## Practice

Write `guessing_game.py`: the computer picks a secret number (use `import random; secret = random.randint(1, 10)`) and the player keeps guessing until they get it right.
