class Car:
    def __init__(self, brand, model, color, mileage):
        self.brand = brand
        self.model = model
        self.color = color
        self.mileage = mileage

CarA = Car('BMW', 'iX3', 'Black', 805)
CarB = Car('Audi', 'Q5', 'White', 700)


print(f'Car A is a {CarA.brand} {CarA.model} in the color {CarA.color} and has a max range of {CarA.mileage}\n Car B is a {CarB.brand} {CarB.model} in the color {CarB.color} and has a max range of {CarB.mileage}')