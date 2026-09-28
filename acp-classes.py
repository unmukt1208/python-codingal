class Pet:
    def __init__(self, name, animal_type, age):
        self.name = name
        self.age = age
        self.animal_type = animal_type
        self.age = age

pet1= Pet("Poppy", "Parrot", 2)
pet2= Pet("Ruffles", "Dog", 5)

print(f'The first pet is called {pet1.name} and is {pet1.age} years old. He is a {pet1.animal_type}\n The second pet is called {pet2.name} and is {pet2.age} years old. He is a {pet2.animal_type}')