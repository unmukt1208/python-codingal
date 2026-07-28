running = True
chore_list = []
while running:
    user_inp = int(input('Enter 1 to add to chore list,\n enter 2 to remove from chore list,\n enter 3 to remove all from chore list\n 4 is to print \n and enter 0 to quit: '))
    if user_inp == 1:
        add = input('What would you like to add?: ')
        chore_list.append(add)
    if user_inp == 2:
        remove = input('What would you like to remove?: ')
        chore_list.remove(remove)
    if user_inp == 3:
        chore_list = []
    if user_inp == 4:
        for i in range(len(chore_list)):
            print(f'{i+1} {chore_list[i]}')
        
    if user_inp == 0:
        break


    
