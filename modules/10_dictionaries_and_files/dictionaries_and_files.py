# dictionaries_and_files.py — Module 10
import json

# --- Dictionaries ---

model = {
    "name": "llama3",
    "size": "8B",
    "context_length": 8192,
    "is_free": True,
}

print(model["name"])
print(model.get("author", "N/A"))

# Add, update, delete
model["quantization"] = "Q4_K_M"
model["size"] = "8.03B"
del model["is_free"]
print(model)

# Iterate
for key, value in model.items():
    print(f"{key}: {value}")

# Nested dictionaries
catalog = {
    "llama3":  {"size": "8B",   "language": "English"},
    "mistral": {"size": "7B",   "language": "Multi"},
    "phi3":    {"size": "3.8B", "language": "English"},
}
print(catalog["mistral"]["language"])

# --- Files ---

# Write
with open("notes.txt", "w") as f:
    f.write("My AI course notes\n")
    f.write("Dictionaries are key-value stores.\n")

# Read
with open("notes.txt", "r") as f:
    print(f.read())

# Append
with open("notes.txt", "a") as f:
    f.write("Files are great for persistence.\n")

# Read line by line
with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())

# JSON
data = {"model": "llama3", "tokens": 1024}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

with open("data.json", "r") as f:
    loaded = json.load(f)
    print(loaded["model"])
