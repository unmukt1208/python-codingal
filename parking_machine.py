print('Your parking fee costs 3 credits')
print('Accepted coins : 0.5, 1, 2 \n \n')
total = 0


while True:
    user_money = float(input('INSERT A COIN: '))
    total += user_money
    print(f'The total so far is {total}')
    if total >= 3:
        break

if total == 3:
    print('No change needs to be given. Enjoy your day')
else:
    change = total - 3
    print(f'The change amount is {change}. Enjoy your day')