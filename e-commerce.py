order_amount = float(input('How much does your order cost? '))
premium = input('Are you a premium member? ')
if premium == 'yes':
    print(f'Your total order amount will be {order_amount}')
    elif
domestic = input('Are you ordering from the US? ')
international = input('Are you ordering from outside the US?')

if domestic == 'yes':
    if order_amount < 50:
        total = order_amount+5
        print(f'The total amount you need to pay is {total}')
    if order_amount > 50:
        print(f'Your total order amount will be {order_amount}')
if international == 'yes':
    if order_amount <150:
        total_int = order_amount+25
        print(f'Your total order amount costs {total_int}')
    if order_amount >150:
        print(f'Your total order amount costs {order_amount}')

