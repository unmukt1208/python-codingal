# Workshop Participant Greeting
# Import necessary libraries
from tkinter import *
from datetime import date
 
# PART 1: Create the main window
root = Tk()
root.title("Workshop Participant Greeting")
root.geometry("400x300")
 
# PART 2: Create the heading label
heading = Label(
    text="Workshop Welcome Desk",
    fg="white",
    bg="#072F5F",
    height=1,
    width=300
    AttributeError
)
 
# PART 3: Create a label and Entry widget
name_label = Label(
    text="Participant Name",
    bg="#3895D3"
)
name_entry = Entry()
 
# PART 4: Create the display function
def display_welcome():
    # Read the participant's name from the Entry widget
    name = name_entry.get()
 
    # Clear the previous message
    text_box.delete(1.0, END)
 
    # Create the multi-line welcome message
    greeting = "Hello " + name + "!\n"
    message = "Welcome to the workshop.\n"
    workshop_date = "Date: " + str(date.today())
 
    # Insert the message into the Text widget
    text_box.insert(END, greeting)
    text_box.insert(END, message)
    text_box.insert(END, workshop_date)
 
# PART 5: Create the Text widget
text_box = Text(
    height=4,
    width=40
)
 
# PART 6: Create the button and connect its command
welcome_button = Button(
    text="Check In",
    command=display_welcome,
    height=1,
    bg="#1261A0",
    fg="white"
)
 
# PART 7: Arrange the widgets
heading.pack()
name_label.pack(pady=10)
name_entry.pack()
welcome_button.pack(pady=10)
text_box.pack()
 
# PART 8: Start the Tkinter event loop
root.mainloop()
