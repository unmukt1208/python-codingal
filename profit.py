buying = float(input('Enter buying amount: '))
selling = float(input('Enter selling amount: '))
if selling>buying:
    profit = selling-buying
    print(f'You made a profit of {profit}')
elif buying>selling:
    loss = buying-selling
    print(f'You made a loss of {loss}')
else:
    print('You didnt make a profit or a loss')
