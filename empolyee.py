from enum import Enum;

Gender = Enum('Gender', ['Male', 'Female']);

class Employee:
    
    def __init__(self, name: str, gender: Gender) -> None:
        self.name = name
        self.gender = gender