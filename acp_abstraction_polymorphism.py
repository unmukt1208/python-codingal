from abc import ABC, abstractmethod

class smart_device(ABC):
    @abstractmethod
    def turn_on(self):
        pass

class light(smart_device):
    def turn_on(self):
        print('Light is on')

class fan(smart_device):
    def turn_on(self):
        print('Fan is on')

class ac(smart_device):
    def turn_on(self):
        print('AC is on')

light = light()
light.turn_on()

fan = fan()
fan.turn_on()

ac = ac()
ac.turn_on()