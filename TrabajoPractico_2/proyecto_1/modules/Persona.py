from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, nombre, edad, dni=None):
        self.nombre = nombre
        self.edad = edad
        self.dni = dni  # DNI es un atributo privado

    
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser una cadena de texto.")

        if not valor.strip():
            raise ValueError("El nombre debe ser una cadena de texto no vacía.")

        self.__nombre = valor.strip()

    @property
    def dni(self):
        return self.__dni
    
    @dni.setter
    def dni(self, valor):
        if valor is not None:
            if not isinstance(valor, str):
                raise TypeError("El DNI debe ser una cadena de texto.")

            if not valor.strip():
                raise ValueError("El DNI debe ser una cadena de texto no vacía.")

        self.__dni = valor.strip() if valor is not None else None