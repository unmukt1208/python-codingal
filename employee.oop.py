class Employee:
    def __init__(self, name):
        self.name = name
        print(f'Employee created: {self.name}')


    def __del__(self):
        print('Destructor called')

def create_obj():
    obj = Employee('Unmukt')
    return obj

print('Calling create obj() function... ')
obj = create_obj()
del obj
print(obj.name)
print('Programme end...')