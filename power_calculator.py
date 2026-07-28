val = int(input('Choose base number: '))
exp = int(input('Choose the exponent power: '))
mul = 1

# product = val**exp
for i in range(exp):
    mul *= val
    

print(f'{val} to the power {exp} equals to {mul}')