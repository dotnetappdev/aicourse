"""Season 1 — Practice Project Solution

Asks the user for their name and a number 1-10,
prints a message based on the range, and saves
the result to results.txt.
"""


def categorize(number: int) -> str:
    """Return a category string based on the number."""
    if number <= 3:
        return "low"
    elif number <= 7:
        return "medium"
    else:
        return "high"


def main():
    name = input("What is your name? ")

    while True:
        raw = input("Enter a number between 1 and 10: ")
        if raw.isdigit() and 1 <= int(raw) <= 10:
            number = int(raw)
            break
        print("Please enter a whole number from 1 to 10.")

    category = categorize(number)
    print(f"Hi {name}! Your number {number} is {category}.")

    with open("results.txt", "w") as f:
        f.write(f"Name: {name}\n")
        f.write(f"Number: {number}\n")
        f.write(f"Category: {category}\n")

    print("Results saved to results.txt")


if __name__ == "__main__":
    main()
