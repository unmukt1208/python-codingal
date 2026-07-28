val = int(input('Enter  Starting Value: '))
end = int(input('Enter Ending Value:  '))
skip = int(input('Enter Skipping Value: '))

i = val
while i < end+1:
    print(i)
    i += skip