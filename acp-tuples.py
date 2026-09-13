# Create a tuple with different data types
habit_info = ("Reading", True, 7, 20.5)
print(habit_info)
 
# Create a tuple of daily habit completion
# 1 means completed, 0 means missed
weekly_habits = (1, 0, 1, 1, 0, 1, 1)
print(weekly_habits)
 
# Find the length of the tuple
print("Total days tracked:", len(weekly_habits))
 
# Access items using indexing
print("Day 1 status:", weekly_habits[0])
print("Day 4 status:", weekly_habits[3])
 
# Access a range using slicing
first_three_days = weekly_habits[0:3]
print("First three days:", first_three_days)
 
weekend_days = weekly_habits[5:7]
print("Weekend days:", weekend_days)
 
# Tuples are immutable, so we cannot directly add a new item
# But we can create a new tuple using the + operator
weekly_habits = weekly_habits + (1,)
print("After adding one more day:", weekly_habits)
 
# Count completed and missed days
completed = weekly_habits.count(1)
missed = weekly_habits.count(0)
 
print("Completed days:", completed)
print("Missed days:", missed)
 
# Check each day using indexing
done = 0
not_done = 0
 
for i in range(0, len(weekly_habits)):
    if weekly_habits[i] == 1:
        done += 1
    else:
        not_done += 1
 
if done > not_done:
    print("Great habit progress!")
else:
    print("Try to be more consistent!")
 
# Final habit tracker summary
print("")
print("===== WEEKLY HABIT TRACKER =====")
print("Habit Name:", habit_info[0])
print("Weekly Record:", weekly_habits)
print("Completed:", done)
print("Missed:", not_done)
print("================================")
