class Parrot:
    specie = 'Bird'
    
    def __init__(self, age, name):
        self.age = age
        self.name = name

ParrotA = Parrot(2, 'Jim')
ParrotB = Parrot(4, 'Poppy')

print(f'Parrot A is {ParrotA.age} years old and is called {ParrotA.name}\n Parrot B is {ParrotB.age} years old and is called {ParrotB.name}')
print(f'The species is {Parrot.specie}')

