grades = {
    "Alice": 88,
    "Bob": 73,
    "Charlie": 95,
    "Diana": 81,
    "Ethan": 64,
}

print("STUDENT GRADE BOOK\n")

print("Select an option:")
print("1 - Look up a student's grade")
print("2 - View class average")
print("3 - View top and bottom student")
print("4 - Exit")

choice = input("\nEnter choice (1-4): ")

if choice == "1":
    search_name = input("Enter a student name to look up: ")
    score = grades.get(search_name, None)
    if score != None:
        print(f"{search_name}'s score: {score}")
    else:
        print(f"Sorry, student '{search_name}' was not found in the grade book.")

elif choice == "2":
    total = 0
    for score in grades.values():
        total += score
    average = total / len(grades)
    print(f"Class Average: {average:.1f}")

elif choice == "3":
    top_student = max(grades, key=grades.get)
    bottom_student = min(grades, key=grades.get)
    print(f"Top Student: {top_student} ({grades[top_student]})")
    print(f"Bottom Student: {bottom_student} ({grades[bottom_student]})")

elif choice == "4":
    print("Exiting program.")

else:
    print("Invalid choice. Please select a number from 1 to 4.")