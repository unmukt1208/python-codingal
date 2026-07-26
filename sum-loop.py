s = int(input('Choose a starting number: '))
e = int(input('Choose an ending number: '))
sum = 0

for i in range (s,e+1):
   sum += i

print(f'Sum equals to {sum}')

