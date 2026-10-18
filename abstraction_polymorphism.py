# Create an abstract base class named Instrument using the abc module with an abstract method called play_sound(). Next, create three subclasses—Guitar, Piano, and Flute—that inherit from Instrument and provide their own unique implementation of the play_sound() method. Finally, write driver code that creates instances of these classes and calls the play_sound() method on each, demonstrating both abstraction and polymorphism.

from abc import ABC, abstractmethod

class Instrument(ABC):
    @abstractmethod
    def play_sound(self):
        pass

class Guitar(Instrument):
    def play_sound(self):
        print('This is a sound the guitar makes: ')

class Piano(Instrument):
    def play_sound(self):
        print('This is a sound the piano makes: ')

class Flute(Instrument):
    def play_sound(self):
        print('This is a sound the flute makes: ')

sound_obj = Guitar()
sound_obj.play_sound()

sound_obj = Piano()
sound_obj.play_sound()

sound_obj = Flute()
sound_obj.play_sound()

