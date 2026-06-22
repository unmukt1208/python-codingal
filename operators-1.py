science = float(input("Enter Science Marks /100: "))
math = float(input("Enter Math Marks /100: "))
german = float(input("Enter German Marks /100: "))
computer = float(input("Enter Computer Marks /100: "))
total_marks = science+math+german+computer
avg_marks = (science+math+german+computer)/4
full_marks = 400
percentage_marks = ((total_marks/full_marks)*100)

print(f'Your total marks are {total_marks}')
print(f'Your average marks are {avg_marks}')
print(f'The percentage you got was {percentage_marks}%')