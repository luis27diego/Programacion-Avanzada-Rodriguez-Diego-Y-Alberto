from .Alimentos import Verdura
#from Frutas import Kiwi, Manzana
import math

class Papa(Verdura):
    def __init__(self, peso):
        super().__init__("Papa", peso)
    
    def calcular_aw(self):
        C = 18  # kg^-1
        resultado = 0.66 * math.atan(C * self.gramos_a_kilos(self._peso))
        return max(0, min(1, resultado))  # Limita entre 0 y 1

class Zanahoria(Verdura):
    def __init__(self, peso):
        super().__init__("Zanahoria", peso)
    
    def calcular_aw(self):
        C = 10  # kg^-1
        resultado = 0.96 * (1 - math.exp(-C * self.gramos_a_kilos(self._peso)))
        return max(0, min(1, resultado))  # Limita entre 0 y 1


# Ejemplo de uso
if __name__ == "__main__":
    # Crear algunos alimentos
    try:
        kiwi = Kiwi(150)
        manzana = Manzana(200)
        papa = Papa(300)
        zanahoria = Zanahoria(100)
        
        print("=== Ejemplos de Alimentos ===")
        alimentos = [kiwi, manzana, papa, zanahoria]
        
        for alimento in alimentos:
            print(f"{alimento}")
            print(f"  Susceptible? {'Si' if alimento.es_susceptible() else 'No'}")
            print()
    except ValueError as e:
        print(f"Error: {e}")    