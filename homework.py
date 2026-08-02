running = True
Homework = []
while running:
    user_homework = int(input('Enter 1 to add to homework list, \n Enter 2 to remove somethign from the homework list \n Enter 3 to remove all from the Homework lsit \n Enter 4 to print all \n Enter 5 to end.: '))
    if user_homework == 1:
        work = input('What would you like to add: ')
        Homework.append(work)
    if user_homework == 2:
        remove = input('What would you like to remove: ')
        Homework.remove(remove)
    if user_homework == 3:
        Homework = []
    if user_homework == 4:
        print(Homework)
    if user_homework == 5:
        break
    