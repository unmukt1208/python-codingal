def greet_mssg():
    print('Welcome to the lemonade stand!')
def thanks_mssg():
    print('Thank you for buying our lemonade')
def calculate_total(user_price,user_quantity):
    total = user_price * user_quantity
    return total
def calculate_change(total):
    customer_money = int(input('How much money is the customer paying?: '))
    change = customer_money - total
    return change
greet_mssg()
user_price = int(input('How much does a lemonade cost?: '))
user_quantity = int(input('How many lemonades is the customer purchasing: '))
total = calculate_total(user_price, user_quantity)
print(f'Total due payment is {total}')
print(f'Lemonade Receipt \n Cup price = {user_price}\n Amount of cups purchased = {user_quantity}\n Change needed to be given = {calculate_change(total)}\n')
thanks_mssg()

