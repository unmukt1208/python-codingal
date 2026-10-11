# Create a SmartAccount class that includes a private balance, a private PIN, and a private method to calculate a transaction fee, along with public methods to deposit funds, securely withdraw funds using the PIN, and check the current balance. then create an instance of the class and check all the methods

class SmartAccount:
    def __init__(self, balance, pin):
        self.__balance = balance 
        self.__pin = pin
        
    
    def __calculate_fee(self):
        fee = 0.02 * self.__balance
        return fee
    

