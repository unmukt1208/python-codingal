day = input('Which day is it (Monday, Tuesday, Wednesday etc.: )')

if day == 'Saturday' or day == 'Sunday':
    weather = input('What is the weather like?(Sunny, Cludy, Rainy etc): ')
 
else:
    weather = input('What is the weather like?(Sunny, Cludy, Rainy etc): ')
 

if weather == 'Sunny':
    homework = input('Have you done your homework? ')
 
if weather == 'Cloudy' or weather == 'Rainy':
    homework = input('Have you done your homework? ')
 
if homework == 'yes':
    print('Homework done, enjoy')
else:
    print('Finish homework. before doing the activities')
  
if day == 'Saturday' or 'Sunday':
    print('Weekend - Enjoy your free time!')
else:
  print('Weekday - Geat Ready for School!')

if weather == 'Sunny':
    print("Sunny - Have fun outside")
else:
    print('Bad weather, consider bringing an umbrella')
 


  
