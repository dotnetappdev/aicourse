# strings.py — Module 03

# Creating strings
single = 'Hello'
double = "World"
multi  = """This string
spans multiple
lines."""

print(single)
print(double)
print(multi)

# Common operations
greeting = "hello world"
print(len(greeting))
print(greeting.upper())
print(greeting.title())
print(greeting.replace("world", "Python"))
print(greeting.split(" "))
print("  spaces  ".strip())

# Concatenation
first    = "Hello"
second   = "World"
combined = first + " " + second
print(combined)

# F-strings
name = "Alice"
age  = 30
print(f"My name is {name} and I am {age} years old.")
print(f"Next year I will be {age + 1}.")
print(f"Name has {len(name)} letters.")

# Checking contents
sentence = "Python is great for AI"
print("Python" in sentence)
print("Java"   in sentence)
print(sentence.startswith("Python"))
print(sentence.endswith("AI"))

# Practice: personalised greeting
user_name = input("What is your name? ")
print(f"Welcome, {user_name}! Let's learn Python.")
