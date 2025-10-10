from modules.Alimentos import Verdura
#from Frutas import Kiwi, Manzana
import math

class Papa(Verdura):
    def __init__(self, peso):
        super().__init__("Papa", peso)
    
    def calcular_aw(self):
        C = 18  # kg^-1
        resultado = 0.66 * math.atan(C * self._peso)
        return max(0, min(1, resultado))  # Limita entre 0 y 1

class Zanahoria(Verdura):
    def __init__(self, peso):
        super().__init__("Zanahoria", peso)
    
    def calcular_aw(self):
        C = 10  # kg^-1
        resultado = 0.96 * (1 - math.exp(-C * self._peso))
        return max(0, min(1, resultado))  # Limita entre 0 y 1

""" 
# Ejemplo de uso
if __name__ == "__main__":

    try:
        papa = Papa(120)
        zanahoria = Zanahoria(200)
        
        print("=== Ejemplos de Alimentos ===")
        alimentos = [papa, zanahoria]
        
        for alimento in alimentos:
            print(f"{alimento}")
            print(f"  Susceptible? {'Si' if alimento.es_susceptible() else 'No'}")
            print()
    except ValueError as e:
        print(f"Error: {e}")     """