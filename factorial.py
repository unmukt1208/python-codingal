def find_factorial(num):
    if num == 0 or num == 1:
        return 1
    else:
        return find_factorial(num-1)*num 
num = int(input('Enter a number to find its factorial: '))
print(f'The factorial of {num} is {find_factorial(num)}')