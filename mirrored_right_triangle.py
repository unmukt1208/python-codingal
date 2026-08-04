n = int(input('Enter amount of rows: \n'))
special_character = input('Enter a special character: \n')



for i in range(n):
    for k in range(n):
        print(' ', end = '')
   
    for j in range(i+1):
        
        print(special_character, end='')
        
    print()
