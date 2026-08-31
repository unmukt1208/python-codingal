try:
    number = int(input('Enter a number: '))
    print(f'Ther number entered is {number}')
except ValueError as ex:
    print('Exception: ', ex)