# lists.py — Module 09

# Creating and accessing
models = ["llama3", "mistral", "phi3", "gemma"]
print(models[0])
print(models[-1])
print(models[1:3])
print(len(models))

# Modifying
models.append("qwen2")
models.insert(1, "codellama")
models.remove("phi3")
popped = models.pop()
print(popped)
models[0] = "llama3.2"

# Useful methods
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print(numbers)
numbers.reverse()
print(numbers)
print(numbers.count(1))
print(numbers.index(5))

# List comprehensions
names  = ["alice", "bob", "charlie"]
upper  = [name.upper() for name in names]
long   = [name for name in names if len(name) > 4]
print(upper)
print(long)

# Membership check
if "qwen2" in models:
    print("qwen2 is available")
