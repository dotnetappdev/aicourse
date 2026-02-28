# while_loops.py — Module 07
import random

# Basic while loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1
print("Done!")

# User-input loop
while True:
    answer = input("Type 'yes' or 'no': ").lower()
    if answer in ("yes", "no"):
        break
    print("Invalid input, try again.")
print(f"You chose: {answer}")

# Countdown
countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
print("Liftoff!")

# Guessing game (practice project built in)
secret = random.randint(1, 10)
attempts = 0

while True:
    guess = int(input("Guess a number between 1 and 10: "))
    attempts += 1
    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")
    else:
        print(f"Correct! You got it in {attempts} attempt(s).")
        break
