# Create a Python program with a base class named Employee that initializes name and base_salary, and includes a method show_details to print these attributes. Then, create a child class named Developer that inherits from Employee, initializes programming_language, name, and base_salary, and overrides show_details using super() to print all details. Additionally, add a method named write_code in Developer that prints a task message, and conclude by checking whether Developer is a subclass of Employee
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def show_traits(self):
        print("Name: ", self.name)
        print("Base Salary:", self.base_salary)

class Developer(Employee):
    def __init__(self, programming_language, name, base_salary):
        self.programming_language = programming_language
        self.name = name
        self.base_salary = base_salary
        super().__init__(name, base_salary)
    
    def show_traits(self):
        print("Name: ", self.name)
        print("Base Salary", self.base_salary)
        super().show_traits()

    def write_code(self):
        print('Working on a project')

child = Developer("Python", "Unmukt", "200,000")
child.show_traits()
child.write_code()
print("Is Developer a Subclass of Employee?", issubclass(Developer, Employee))
