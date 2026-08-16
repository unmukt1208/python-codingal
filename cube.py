def cube(num):
    cube_val = num*num*num
    if cube_val % 3 == 0:
        print('The cube value is divisible by 3')
    else:
        print('The cube value is not divisible by 3')
num = int(input('Enter your desired number to cube: '))
cube(num)
