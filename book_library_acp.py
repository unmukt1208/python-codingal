
class Book:

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def borrow(self):
        if self.is_borrowed:
            print(f"'{self.title}' is already borrowed.")
        else:
            self.is_borrowed = True
            print(f"You have successfully borrowed '{self.title}'.")

    def return_book(self):
        if not self.is_borrowed:
            print(f"'{self.title}' was not borrowed.")
        else:
            self.is_borrowed = False
            print(f"You have successfully returned '{self.title}'.")

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"{self.title} by {self.author} [{status}]"



book1 = Book("Python Crash Course", "Eric Matthes")
book2 = Book("Automate the Boring Stuff", "Al Sweigart")
book3 = Book("Fluent Python", "Luciano Ramalho")

print("=" * 42)
print("         📚  LIBRARY SYSTEM")
print("=" * 42)



print(book1)
print(book2)
print(book3)


book1.borrow()
book2.borrow() 
book3.borrow()


book1.return_book()
book2.return_book() 
book3.return_book()



print(book1)
print(book2)
print(book3)