s = int(input('Choose a starting number: '))
e = int(input('Choose an ending number: '))
sum = 0

for i in range (s,e+1):
   if i%2==0:
      sum += i


print(f'The even numbers in this range are {sum}')
   
   
