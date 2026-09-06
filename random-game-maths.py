# Random Fun Calculator

# PART 1: Import random and math modules
import random
import math

print("===== RANDOM FUN CALCULATOR =====")

# PART 2: Generate a random lucky number using randint()
lucky_number = random.randint(1, 10)
print("Your lucky number is:", lucky_number)

# PART 3: Turn a random number into a random choice
fun_choices = ["Play a game", "Solve a puzzle", "Read a story", "Draw something"]
random_activity = random.choice(fun_choices)
print("Random activity for today:", random_activity)

# PART 4: Number guessing game
print("\nGuess the secret number from 1 to 5!")
secret_number = random.randint(1, 5)

while True:
    guess = int(input("Enter your guess: "))

    if guess == secret_number:
        print("Correct! You guessed the number.")
        break
    else:
        print("Wrong guess. Try again!")

# PART 5: Use math module functions
decimal_number = float(input("\nEnter a decimal number: "))

print("Ceiling value:", math.ceil(decimal_number))
print("Floor value:", math.floor(decimal_number))

# PART 6: Use copysign()
x = 10
y = -5
print("Copy sign result:", math.copysign(x, y))

# PART 7: Use fabs()
negative_number = int(input("Enter a negative number: "))
print("Absolute value:", math.fabs(negative_number))

# PART 8: Use gcd()
num1 = int(input("Enter first number for GCD: "))
num2 = int(input("Enter second number for GCD: "))

print("GCD is:", math.gcd(num1, num2))

# PART 9: Print final summary
print("\n===== FUN CALCULATOR SUMMARY =====")
print("Lucky Number:", lucky_number)
print("Random Activity:", random_activity)
print("Secret Number:", secret_number)
print("==================================")
