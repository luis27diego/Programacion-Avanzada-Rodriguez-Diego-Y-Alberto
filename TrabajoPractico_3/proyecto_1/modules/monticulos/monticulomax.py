

class MonticuloMaximo:
    def __init__(self):
        self.listaMonticulo = [0]
        self.tamanoActual = 0

    # 1. El nuevo elemento "sube" hasta que encuentra un padre MAYOR.
    def infiltArriba(self, i):
        while i // 2 > 0:
            # ¡CAMBIO! Comparamos si el hijo es MAYOR que el padre.
            if self.listaMonticulo[i] > self.listaMonticulo[i // 2]:
                # Intercambio (swap)
                tmp = self.listaMonticulo[i // 2]
                self.listaMonticulo[i // 2] = self.listaMonticulo[i]
                self.listaMonticulo[i] = tmp
            i = i // 2

    def insertar(self, k):
        self.listaMonticulo.append(k)
        self.tamanoActual = self.tamanoActual + 1
        self.infiltArriba(self.tamanoActual)

    # 2. Encuentra el hijo MÁS GRANDE para comparar con el padre.
    def hijoMax(self, i):
        # Si no hay hijo derecho, el hijo izquierdo es el único.
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        else:
            # ¡CAMBIO! Retornamos el índice del hijo MAYOR.
            if self.listaMonticulo[i * 2] > self.listaMonticulo[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1
    
    # Hemos renombrado 'hijoMin' a 'hijoMax' para claridad, pero la función es la misma.
    # El método original 'hijoMin' en el Montículo de Mínimos buscaba el mínimo;
    # este busca el máximo.

    # 3. El nuevo elemento de la raíz "baja" hasta que encuentra hijos MENORES.
    def infiltAbajo(self, i):
        # Usamos hijoMax para obtener el índice del hijo mayor.
        while (i * 2) <= self.tamanoActual:
            hm = self.hijoMax(i)
            # ¡CAMBIO! Comparamos si el padre es MENOR que el hijo mayor.
            if self.listaMonticulo[i] < self.listaMonticulo[hm]:
                # Intercambio (swap)
                tmp = self.listaMonticulo[i]
                self.listaMonticulo[i] = self.listaMonticulo[hm]
                self.listaMonticulo[hm] = tmp
            i = hm

    # El método 'eliminarMax' elimina la raíz, que es el elemento MÁXIMO.
    def eliminarMax(self):
        # La raíz (índice 1) es el elemento máximo.
        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual = self.tamanoActual - 1
        self.listaMonticulo.pop()
        self.infiltAbajo(1) # Llama a infiltAbajo para reordenar
        return valorSacado

    def construirMonticulo(self, unaLista):
        i = len(unaLista) // 2
        self.tamanoActual = len(unaLista)
        self.listaMonticulo = [0] + unaLista[:]
        while (i > 0):
            self.infiltAbajo(i) # Llama a infiltAbajo, que usa hijoMax
            i = i - 1
