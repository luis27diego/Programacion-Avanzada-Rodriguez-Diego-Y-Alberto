from abc import ABC, abstractmethod

class Alimento(ABC):
    """Clase abstracta base para todos los alimentos"""
    
    def __init__(self, nombre, peso):
        self._nombre = nombre
        self.peso = peso  # Usa el setter para validación
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def peso(self):
        return self._peso
    
    @peso.setter
    def peso(self, valor):
        if valor <= 0:
            raise ValueError(f"El peso debe ser mayor a 0, recibido: {valor}")
        if valor >= 600:
            raise ValueError(f"El peso debe ser menor a 600g para cálculos válidos, recibido: {valor}")
        self._peso = valor
    
    @abstractmethod
    def calcular_aw(self):
        """Método abstracto para calcular la actividad acuosa"""
        pass
    
    def es_susceptible(self):
        """Verifica si el alimento es susceptible a microorganismos (aw > 0.90)"""
        return self.calcular_aw() > 0.90

    def gramos_a_kilos(self, gramos):
        """Convierte gramos a kilogramos"""
        return gramos 

    def __str__(self):
        return f"{self._nombre} ({self._peso}g) - aw: {self.calcular_aw():.3f}"

class Fruta(Alimento):
    """Clase abstracta para frutas"""
    pass


class Verdura(Alimento):
    """Clase abstracta para verduras"""
    pass