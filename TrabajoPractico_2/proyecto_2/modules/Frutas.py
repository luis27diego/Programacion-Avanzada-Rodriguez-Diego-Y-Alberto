from Alimentos import Fruta
import math

class Kiwi(Fruta):
    def __init__(self, peso):
        super().__init__("Kiwi", peso)
    
    def calcular_aw(self):
        C = 18  # kg^-1
        exponente = -C * self.gramos_a_kilos(self._peso)
        numerador = 1 - math.exp(exponente)
        denominador = 1 + math.exp(exponente)
        resultado = 0.96 * (numerador / denominador)
        return max(0, min(1, resultado))  # Limita entre 0 y 1


class Manzana(Fruta):
    def __init__(self, peso):
        super().__init__("Manzana", peso)
    
    def calcular_aw(self):
        C = 15  # kg^-1
        Cm = C * self.gramos_a_kilos(self._peso)
        resultado = 0.97 * (Cm**2) / (1 + Cm**2)
        return max(0, min(1, resultado))  # Limita entre 0 y 1
