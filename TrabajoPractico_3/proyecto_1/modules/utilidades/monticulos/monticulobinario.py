from modules.utilidades.monticulos.monticulomin import MonticuloMin
from modules.utilidades.monticulos.monticulomax import MonticuloMaximo

class MonticuloMedianaBinario():
    def __init__(self):
      self._valor_mediana = 0
      self.__monticulo_min = MonticuloMin()
      self.__monticulo_max = MonticuloMaximo()
    @property
    def valor_mediana(self):
        return self._valor_mediana
    def insertar(self, valor):
        if valor > self.valor_mediana:
            self.__monticulo_min.insertar(valor)
        else:
            self.__monticulo_max.insertar(valor)

        # Balancear los montículos
        self.__balancear()

    def __balancear(self):
        # maxHeap puede tener como máximo 1 elemento más que minHeap
        if self.__monticulo_max.tamanoActual > self.__monticulo_min.tamanoActual + 1:
            self.__monticulo_min.insertar(self.__monticulo_max.eliminarMax())

        elif self.__monticulo_min.tamanoActual > self.__monticulo_max.tamanoActual + 1:
            self.__monticulo_max.insertar(self.__monticulo_min.eliminarMin())

        self.__actualizar_mediana()

    def __actualizar_mediana(self):
                
        # Si hay un número par de elementos, la mediana está en maxHeap
        if self.__monticulo_max.tamanoActual == self.__monticulo_min.tamanoActual:
            self._valor_mediana = (self.__monticulo_min.listaMonticulo[1] + self.__monticulo_max.listaMonticulo[1]) / 2

        else:
            # Si hay un número impar, obtener el montículo con mayor tamaño
            if self.__monticulo_max.tamanoActual > self.__monticulo_min.tamanoActual:
                mayor = self.__monticulo_max
            else:
                mayor = self.__monticulo_min
            self._valor_mediana = mayor.listaMonticulo[1]

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