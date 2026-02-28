# Season 1 — Python Fundamentals
### "Everything You Need to Know Before Touching AI"
**Estimated runtime: ~30 minutes**

---

## Pre-Roll (0:00 – 0:45)

*[Upbeat intro music. Screen shows the course logo.]*

**Host (on camera):**
Hey, welcome! I'm so glad you're here.

In this course we are going to take you from absolute zero — no programming experience required — all the way to building real AI-powered applications that run **entirely on your own computer**, using free, open-source tools.

Before we touch any AI, we need to speak its language. And that language is **Python**. Don't worry — Python is one of the most beginner-friendly programming languages in the world, and today we're only going to learn the parts you actually need.

Let's dive in.

---

## Episode 1 — Your First Python Program (0:45 – 8:00)

### Setting Up (0:45 – 2:30)

*[Screen share: browser open to python.org/downloads]*

**Host (voiceover):**
First, let's make sure Python is installed. Head to python.org/downloads and grab version 3.10 or newer. Run the installer — on Windows, make sure to check **"Add Python to PATH"** before clicking Install.

Once that's done, open a terminal. On Windows that's **PowerShell** or **Command Prompt**. On Mac or Linux it's **Terminal**.

Type:

```
python --version
```

You should see something like `Python 3.11.5`. Perfect.

Now open your favorite code editor. I'll be using **VS Code** throughout this course, which is free at code.visualstudio.com. Install the **Python extension** from the Extensions sidebar.

Create a new folder called `aicourse` and open it in VS Code.

### Hello, World! (2:30 – 4:00)

*[Screen share: VS Code with a new file `hello.py`]*

**Host (voiceover):**
Create a new file called `hello.py`. Type this:

```python
print("Hello, World!")
```

Now open a terminal in VS Code — press **Ctrl+`** — and run:

```
python hello.py
```

You should see `Hello, World!` printed in the terminal. Congratulations — you just wrote your first Python program.

`print()` is a **function** — it's a command that tells Python to display something on screen. The text inside the quotes is called a **string**.

### Variables and Data Types (4:00 – 8:00)

**Host (voiceover):**
Programs need to remember things. We store information in **variables**.

```python
# This is a comment — Python ignores it
name = "Alice"          # string (text)
age = 30                # integer (whole number)
temperature = 98.6      # float (decimal number)
is_learning = True      # boolean (True or False)

print(name)
print(age)
print(temperature)
print(is_learning)
```

Notice there are no type declarations — Python figures out the type automatically. That's one reason it's great for beginners.

You can also do math with variables:

```python
x = 10
y = 3

print(x + y)   # 13
print(x - y)   # 7
print(x * y)   # 30
print(x / y)   # 3.333...
print(x // y)  # 3  (integer division)
print(x % y)   # 1  (remainder)
print(x ** y)  # 1000 (power: 10 cubed)
```

And you can combine strings:

```python
first_name = "Alice"
last_name  = "Smith"
full_name  = first_name + " " + last_name
print(full_name)        # Alice Smith

# f-strings are the modern, readable way:
print(f"Hello, {full_name}! You are {age} years old.")
```

---

## Episode 2 — Control Flow and Functions (8:00 – 18:00)

### if / elif / else (8:00 – 11:30)

**Host (voiceover):**
Programs make decisions using **if statements**.

```python
score = 85

if score >= 90:
    print("A — Excellent!")
elif score >= 80:
    print("B — Great job!")
elif score >= 70:
    print("C — Not bad.")
else:
    print("Keep practicing!")
```

Notice the **indentation** — Python uses spaces (usually 4) to group code. This is not optional; Python will error if you get it wrong.

### Loops (11:30 – 14:30)

**Host (voiceover):**
When you need to repeat an action, use a **loop**.

```python
# for loop — iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")

# range() generates a sequence of numbers
for i in range(5):
    print(i)   # prints 0, 1, 2, 3, 4

# while loop — keep going until a condition is False
count = 0
while count < 3:
    print(f"Count is {count}")
    count += 1   # same as: count = count + 1
```

### Functions (14:30 – 18:00)

**Host (voiceover):**
A **function** is a reusable block of code. You define it once and call it whenever you need it.

```python
def greet(name):
    """Say hello to someone."""
    return f"Hello, {name}!"

message = greet("Alice")
print(message)   # Hello, Alice!

# Functions can have default parameter values
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Bob"))             # Hello, Bob!
print(greet("Charlie", "Hi"))   # Hi, Charlie!
```

The text in triple quotes right after `def` is a **docstring** — a short description of what the function does. Get in the habit of writing them.

---

## Episode 3 — Lists, Dicts, and Files (18:00 – 27:00)

### Lists (18:00 – 21:00)

**Host (voiceover):**
A **list** holds multiple values in order.

```python
models = ["llama3", "mistral", "phi3", "gemma"]

print(models[0])          # llama3 (index starts at 0)
print(models[-1])         # gemma  (last item)
print(len(models))        # 4

models.append("qwen2")    # add to end
models.remove("phi3")     # remove by value

# List comprehension — create a new list in one line
upper_models = [m.upper() for m in models]
print(upper_models)
```

### Dictionaries (21:00 – 24:00)

**Host (voiceover):**
A **dictionary** stores key-value pairs — think of it like a real dictionary where you look up a word (key) to get its definition (value).

```python
model_info = {
    "name": "llama3",
    "parameters": "8B",
    "context_length": 8192,
    "is_free": True
}

print(model_info["name"])           # llama3
print(model_info.get("size", "unknown"))  # unknown (safe access)

model_info["quantization"] = "Q4_K_M"    # add new key
print(model_info)
```

Dictionaries are extremely important in AI work because the messages you send to LLMs are structured as dictionaries.

### Reading and Writing Files (24:00 – 27:00)

**Host (voiceover):**
AI applications constantly read and write files — prompts, logs, data.

```python
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
        print(line.strip())  # strip() removes the newline character
```

The `with` statement automatically closes the file when you're done — always use it.

---

## Season Wrap-Up (27:00 – 30:00)

*[Host back on camera]*

**Host:**
Amazing work! In this season you learned:

- ✅ Variables and data types
- ✅ `if` statements and loops
- ✅ Functions with parameters and return values
- ✅ Lists and dictionaries
- ✅ Reading and writing files

That's genuinely everything you need to understand the AI code we're about to write.

In **Season 2** we'll install Ollama, download a real LLM, and have our first conversation with it — all running locally, no internet required.

Drop a comment below with what you built, and I'll see you in the next one!

*[Outro music]*

---

## 🏋️ Practice Project

Create a file called `practice.py` that:
1. Asks the user their name using `input()`
2. Asks them to enter a number between 1 and 10
3. Prints one of three messages depending on whether the number is low (1–3), medium (4–7), or high (8–10)
4. Saves the user's name and their number to a file called `results.txt`

A sample solution is in `code/practice_solution.py`.
