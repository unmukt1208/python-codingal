# PART 1: Create the parent class with shared vehicle details
class Vehicle:
    def __init__(self, brand, max_speed):
        self.brand = brand
        self.max_speed = max_speed

    def show_details(self):
        print("Brand:", self.brand)
        print("Max Speed:", self.max_speed, "km/h")

# PART 2: Create the child class that inherits from Vehicle
class Car(Vehicle):

    # PART 3: Give Car its own details, plus the inherited vehicle details
    def __init__(self, model, seats, brand, max_speed):
        self.model = model
        self.seats = seats
        super().__init__(brand, max_speed)

    # PART 4: Override show_details to add the car's own details too
    def show_details(self):
        print("Model:", self.model)
        print("Seats:", self.seats)
        super().show_details()

    # PART 5: Add a brand new method that only Car has
    def fuel_type(self, fuel):
        print(self.model, "uses", fuel)

# PART 6: Create a Car object with real vehicle values
my_car = Car("City Rider", 5, "Honda", 180)

# PART 7: Call the overridden method and the new method
my_car.show_details()
my_car.fuel_type("petrol")

# PART 8: Check whether Car is really a subclass of Vehicle
print("Is Car a subclass of Vehicle?", issubclass(Car, Vehicle))
