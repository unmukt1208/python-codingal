def greet_mssg():
    print('Welcome to the lemonade stand!')

def thanks_mssg():
    print('Thank you for buying our lemonade')

def calculate_total(user_price, user_quantity):
    total = user_price * user_quantity
    return total

def error_mssg():
    print('Unfortunately we cannot accept your payment as you have not paid enough')

def calculate_change(total):
    customer_money = float(input('How much money is the customer paying?: '))
    change = customer_money - total
    return change

greet_mssg()
user_price = float(input('How much does a lemonade cost?: '))
user_quantity = int(input('How many lemonades is the customer purchasing: '))

total = calculate_total(user_price, user_quantity)
print(f'Total due payment is {total}')

final_change = calculate_change(total)

if final_change < 0:
    error_mssg()
else:
    print(f'\nLemonade Receipt \n Cup price = {user_price}\n Amount of cups purchased = {user_quantity}\n Change needed to be given = {final_change}\n')
    thanks_mssg()




    
