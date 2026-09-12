weather = (1, 0, 0, 0, 1, 1, 0)
sunny = 0
rainy = 0
for i in weather:
    if i == 1:
        rainy += 1
    else:
        sunny += 1
    
if sunny > rainy:
    print('The prediction is sunny')
else:
    print('The prediction is rainy')