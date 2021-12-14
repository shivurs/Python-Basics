class Dog:

    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} is {self.age} years old"

    def speak(self, sound):
        return f"{self.name} barks: {sound}"

class JackRussellTerrier(Dog):
    def speak(self, sound = "Arf"):
        return super().speak(sound)

class BostonTerrier(Dog):
    def speak(self, sound = "What are you lookin at, chump?"):
        return super().speak(sound)




miles = JackRussellTerrier("Miles", 4)
bossman = BostonTerrier("Bossman", 2.5)

print(miles)
print(miles.speak())

print(bossman)
print(bossman.speak())

