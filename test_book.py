class Book:
    def borrow(self):
        is_borrowed = True
        if is_borrowed == True:
            print('This book has been borrowed')
    def return_book(self):
        is_borrowed = False
        if is_borrowed == False:
            print('This book has been returned')

HarryPotter = Book()
HarryPotter.return_book()

LordOfTheRings = Book()
LordOfTheRings.borrow()

PercyJackson = Book()
PercyJackson.return_book()

