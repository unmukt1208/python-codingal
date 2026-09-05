import random
while True:
    user_inp = input(('Enter a choice (Accepted forms = rock, paper, scissors or exit to stop): '))
    if user_inp == 'exit':
        break
    possible_actions = ['rock', 'paper', 'scissors']
    computer_inp = random.choice(possible_actions)
    print(f'You chose {user_inp}, Computer chose {computer_inp}.')
    if user_inp == computer_inp:
        print('There is a tie!')
    else:
        if user_inp == 'rock':
            if computer_inp == 'paper':
                print('The computer won!')
            else:
                print('You won!')
        elif user_inp == 'paper':
            if computer_inp == 'scissors':
                print('The computer won!')
            else:
                print('You won')
        else:
            if computer_inp == 'rock':
                print('The computer won!')
            else:
                print('You won! ')
print('Thanks for playing! ')
    

