name = input('Hi customer! Please enter your name: ')
running = True
while running:
    user_amount = int(input('Welcome to the ATM, how much would you like to withdraw? '))
    denominations = [500, 200, 100, 50, 20, 10, 5, 1]
    remaining_amount = user_amount
    print(f'Hey {name}, this is your withdrawal amount: \n')

        


    for i in denominations:
        count = remaining_amount//i
        if count>0:
            print(f'{count}*{i} = {count*i}')
        remaining_amount %= i
    continuation = input('Would you like to continue for another transaction yes/no: ')
    if continuation == 'no':
        print('Enjoy your day. ATM powering off')
        break

        