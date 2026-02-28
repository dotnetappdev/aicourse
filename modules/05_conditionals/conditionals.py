# conditionals.py — Module 05

# Basic if / else
temperature = 25
if temperature > 30:
    print("It's hot — wear a t-shirt!")
else:
    print("It's comfortable — a light jacket works.")

# if / elif / else
score = 72
if score >= 90:
    print("A — Excellent!")
elif score >= 80:
    print("B — Great job!")
elif score >= 70:
    print("C — Good effort!")
elif score >= 60:
    print("D — Needs improvement.")
else:
    print("F — Please see your instructor.")

# Comparison operators
x = 10
print(x == 10)
print(x != 5)
print(x > 8)
print(x < 8)
print(x >= 10)
print(x <= 9)

# Logical operators
age  = 25
city = "New York"
if age >= 18 and city == "New York":
    print("Eligible for the local program.")
if age < 13 or age > 65:
    print("Special pricing applies.")
if not age < 18:
    print("You are an adult.")

# Ternary
status = "adult" if age >= 18 else "minor"
print(status)
