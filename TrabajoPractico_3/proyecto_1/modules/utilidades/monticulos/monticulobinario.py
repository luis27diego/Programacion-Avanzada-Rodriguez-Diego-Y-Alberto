from modules.utilidades.monticulos.monticulomin import MonticuloBinario
from modules.utilidades.monticulos.monticulomax import MonticuloMaximo

class MonticuloMedianaBinario():
    def __init__(self):
      self.valor_mediana = 0
      self.monticulo_min = MonticuloBinario()
      self.monticulo_max = MonticuloMaximo()

    def insertar(self, valor):
        if valor > self.valor_mediana:
            self.monticulo_min.insertar(valor)
        else:
            self.monticulo_max.insertar(valor)
    
        # Balancear los montículos
        self.balancear()
    
    def balancear(self):
        # maxHeap puede tener como máximo 1 elemento más que minHeap
        if self.monticulo_max.tamanoActual > self.monticulo_min.tamanoActual + 1:
            self.monticulo_min.insertar(self.monticulo_max.eliminarMax())

        elif self.monticulo_min.tamanoActual > self.monticulo_max.tamanoActual + 1:
            self.monticulo_max.insertar(self.monticulo_min.eliminarMin())

        self.actualizar_mediana()

    def actualizar_mediana(self):
        #if self.monticulo_max.estaVacio() and self.monticulo_min.estaVacio():
            #return None
        
        # Si hay un número par de elementos, la mediana está en maxHeap
        if self.monticulo_max.tamanoActual == self.monticulo_min.tamanoActual:
            self.valor_mediana = (self.monticulo_min.listaMonticulo[1] + self.monticulo_max.listaMonticulo[1]) / 2

        else:
            # Si hay un número impar, obtener el montículo con mayor tamaño
            if self.monticulo_max.tamanoActual > self.monticulo_min.tamanoActual:
                mayor = self.monticulo_max
            else:
                mayor = self.monticulo_min
            self.valor_mediana = mayor.listaMonticulo[1]

    def construir_monticulo(self, lista):
        for numero in lista:
            self.insertar(numero)


if __name__ == "__main__":
    monticulomax = MonticuloMaximo()

    monticulomax.insertar(9)
    monticulomax.insertar(5)
    monticulomax.insertar(6)
    monticulomax.insertar(2)
    monticulomax.insertar(3)
    monticulomax.insertar(1)
    monticulomax.insertar(10)
    monticulomax.insertar(8)
    monticulomax.insertar(13)

    print(monticulomax.listaMonticulo)


    monticulo_mediana_binario = MonticuloMedianaBinario()
    datos = [1,2,3,4,5,6,7,8,9,10,11]
    monticulo_mediana_binario.construir_monticulo(datos)
    print(f"Mediana actual: {monticulo_mediana_binario.valor_mediana}")