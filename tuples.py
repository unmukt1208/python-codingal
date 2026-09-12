var_tup = (1, True, 'Hello', 3,78)
int_tup = (2, 5, 7, 9, 9, 2, 5)
user_inp = int(input('Which numbers occurances do you want to find?: '))
count_val = 0
for i in int_tup:
    if i == user_inp:
        count_val += 1



print(f'The number occured {count_val} times')
print(int_tup[1: 5])
    