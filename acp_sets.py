# PART 1: Create two snack boxes as sets
snack_box1 = {"chips", "juice", "cookies", "chips", "apple"}
snack_box2 = {"cookies", "sandwich", "juice", "sandwich"}
print("Snack Box 1:", snack_box1)
print("Snack Box 2:", snack_box2)

# PART 2: Add a new snack to snack_box1
snack_box1.add("banana")
print("Snack Box 1 after adding banana:", snack_box1)

# PART 3: Find snacks common to both boxes
common_snacks = snack_box1.intersection(snack_box2)
print("Snacks in both boxes:", common_snacks)

# PART 4: Create an array of snack counts using the array module
import array as arr
snack_counts = arr.array('i', [4, 6, 3, 5])
print("Snack counts array:", snack_counts)

# PART 5: Add new snack counts to the array
snack_counts.insert(0, 2)
snack_counts.append(7)
print("Snack counts after adding items:", snack_counts)

# PART 6: Count how many times the number 5 appears in the array
count_of_5 = snack_counts.count(5)
print("Number of times 5 appears:", count_of_5)

# PART 7: Reverse the order of the snack counts array
snack_counts.reverse()
print("Reversed snack counts array:", snack_counts)

# PART 8: Print the final school snack counter summary
print("")
print("===== SCHOOL SNACK COUNTER =====")
print("Snack Box 1:", snack_box1)
print("Snack Box 2:", snack_box2)
print("Shared snacks:", common_snacks)
print("Snack counts:", snack_counts)
print("================================")
