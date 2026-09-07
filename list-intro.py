og_list = [1, 5, 7, 8, 10, 12, 14, 15]
while True:
    print(' 1. Display the list \n 2. Reverse the list \n 3. Find the total of the list \n 4. Find the average of the list \n 5. Find the largest element in the list \n 6. Find the smallest element in the list \n 0. Quit')
    user_choice = int(input('Enter a choice in number format: '))

    if user_choice == 1:
        print(og_list)
    elif user_choice == 2:
        print(og_list[::-1])
    elif user_choice == 3:
        sum = 0
        for i in og_list:
            sum += i
        print(f'Total value = {sum}')
    elif user_choice == 4:
        sum = 0
        for i in og_list:
            sum += i
        avg = sum/len(og_list)
        print(f'Average value is {avg}')
    elif user_choice == 5:
        
        print(f'Largest value = {max(og_list)}')
    elif user_choice == 6:
    
        print(f'Smallest value = {min(og_list)}')
    elif user_choice == 0:
        break
    else:
        print('Invalid input!')
    


