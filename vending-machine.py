print('This snack costs 25 credits')
print('Accepted coins : 1, 2, 5, 10, 25\n \n')
total = 0


while True:
    user_money = int(input('INSERT A COIN: '))
    total += user_money
    print(f'The total so far is {total}')
    if total >= 25:
        break

if total == 25:
    print('No change needs to be given. Enjoy your snack/drink')
else:
    change = total - 25
    print(f'The change amount is {change}. Enjoy your snack/drink')


   

