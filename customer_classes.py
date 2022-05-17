import numbers
# from xml.etree.ElementTree import ProcessingInstruction

class Customer:

    def __init__(self, name = "", number = 0, points = 0):
        self.fullname = name.capitalize()
        self.number = number
        self.points = points

    @property
    def fullname(self):
        return self.__fullname.capitalize()
    

    @fullname.setter
    def fullname(self, name):
        if name.isalpha():
            self.__fullname = name
        else:
            self.__fullname = 'N/A'

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number

    def __str__(self):
        return f'Name: {self.fullname}\nNumber: {self.number}\nPoints: {self.points}'
        

