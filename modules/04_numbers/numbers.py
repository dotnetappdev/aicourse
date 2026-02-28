# numbers.py — Module 04
import math

# Arithmetic operators
x = 10
y = 3

print(x + y)    # 13
print(x - y)    # 7
print(x * y)    # 30
print(x / y)    # 3.333...
print(x // y)   # 3
print(x % y)    # 1
print(x ** y)   # 1000

# Even / odd check using modulus
number = 7
if number % 2 == 0:
    print("Even")
else:
    print("Odd")

# Shorthand assignment
score = 100
score += 10
score -= 5
score *= 2
score //= 3
print(score)

# int vs float
print(10 / 2)
print(10 // 2)
print(int(3.9))
print(float(5))
print(round(3.14159, 2))

# Math functions
print(abs(-7))
print(max(3, 7, 1))
print(min(3, 7, 1))
print(sum([1, 2, 3]))
print(math.sqrt(16))
print(math.pi)
