class Duck:

    STREET = "Pond Street"

    def __init__(self, n, a):
        print("Hello from", n)
        self.age = a
        self.name = n

    def make_noise(self):
        print(f"QUACK from {self.name}, {self.age}")
        Duck.STREET = f"{self.name} street"

    def age_me(self):
        self.age += 1

    @classmethod
    def foo(cls):
        print("Class level")

duck1 = Duck("Fred", 45)
duck2 = Duck("Susan", 21)
duck1.age += 2
duck1.make_noise()
duck2.make_noise()
duck2.age_me()
duck2.make_noise()

Duck.foo()