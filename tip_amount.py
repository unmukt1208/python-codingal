def tip(bill_amount):
    tip_amount = bill_amount * 0.05
    return tip_amount
bill_amount = float(input('Enter your bill amount from the restaurant: '))
print(f'The tip amount you should give is {tip(bill_amount)}')