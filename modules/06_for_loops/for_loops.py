# for_loops.py — Module 06

# Loop over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")

# range()
for i in range(5):
    print(i)

for i in range(1, 6):
    print(i)

for i in range(0, 10, 2):
    print(i)

# enumerate()
models = ["llama3", "mistral", "phi3"]
for index, model in enumerate(models):
    print(f"{index + 1}. {model}")

# break
for i in range(10):
    if i == 5:
        break
    print(i)

# continue
for i in range(5):
    if i == 2:
        continue
    print(i)

# List comprehension
squares      = [x ** 2 for x in range(6)]
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
print(squares)
print(even_squares)
