# Write a program that manages student grades using a dictionary by first creating a dictionary named `students` initialized with `"Alice"` (85), `"Bob"` (92), and `"Charlie"` (78), then adding a new student `"Diana"` with a grade of 95, updating `"Charlie"`'s grade to 82, printing the total number of students in the dictionary, and finally looping through the dictionary to print each student's name alongside `"Pass"` if their grade is 80 or higher or `"Needs Improvement"` if it is lower than 80.

students = {'Alice': 85, 'Bob': 92, 'Charlie': 78}
students['Diana'] = 95
print(students)
students['Charlie'] = 72
print('Students')
for i in students:
    if students[i]>=80:
        print('Pass')
    else:
        print('Needs Improvement')