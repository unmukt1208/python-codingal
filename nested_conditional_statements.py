user_vehicle = input('Are you buying a bike or a car(Type 1 for bike and 2 for car)? ')
if user_vehicle == '1':
    type_of_bike = input('Which bike company are you looking to buy from(Type 1 for Royal Enfield, 2 for Suzuki and 3 for Bajaj)? ')
    if type_of_bike == '1':
        print("Congratulations on your new Royal Enfield bike! It has a top speed of 160 km/h. It is suitable for usual city rides.")
    elif type_of_bike == '2':
        print("Congratulations on your new Suzuki bike! It has a top speed of 200 km/h. It is suitable for racing.")
    elif type_of_bike == '3':
        print("Congratulations on your new Bajaj bike! It has a top speed of 130 km/h. It is suitable carrying heavy load.")
    else:
        print('Invalid bike model')

elif user_vehicle == '2':
    type_of_car = input('Which car brand are you looking to buy from(Type 1 for BMW, 2 for Mercedes. 3 for Toyota?) ')
    if type_of_car == '1':
        print('Congratulations on you new BMW car! It has a top speed of 280 km/h. It is suitable for racing.')
    elif type_of_car == '2':
        print('Congratulations on you new Mercedes car! It has a top speed of 200 km/h. It is suitable for comfortable rides.')
    elif type_of_car == '3':
        print('Congratulations on you new Toyota car! It has a top speed of 220 km/h. It is suitable for its affordability.')
    else:
        print('Invalid car model')
else:
    print('Invalid option')
    

    


