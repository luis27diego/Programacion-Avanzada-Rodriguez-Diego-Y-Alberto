import unittest
#from modules.utilidades.monticulos.monticulomin import MonticuloMin
#from modules.utilidades.monticulos.monticulomax import MonticuloMaximo
from modules.utilidades.monticulos.monticulobinario import MonticuloMedianaBinario

# Importar las clases MonticuloMin, MonticuloMaximo y MonticuloMedianaBinario
# Si están en el mismo directorio, ajusta la importación según tu estructura.
# Suponiendo que has pegado las implementaciones de las tres clases aquí...

# --------------------------------------------------------------------------
# --- Implementaciones de MonticuloMin, MonticuloMaximo, y MonticuloMedianaBinario ---
# (Se asume que el código de las tres clases está disponible aquí o importado)
# --------------------------------------------------------------------------

# --- COMIENZO DE LAS PRUEBAS ---

class TestMonticuloMedianaBinario(unittest.TestCase):
    
    def setUp(self):
        """Inicializa una instancia nueva de MonticuloMedianaBinario antes de cada prueba."""
        # Crea una instancia limpia para cada test
        self.monticulo = MonticuloMedianaBinario()

    def test_inicializacion(self):
        """Verifica que los montículos estén vacíos y la mediana sea 0 al inicio."""
        self.assertEqual(self.monticulo.valor_mediana, 0)
        
        # Accediendo a los atributos privados para verificar el estado interno
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_min.tamanoActual, 0)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_max.tamanoActual, 0)

    def test_insertar_un_elemento(self):
        """Prueba la inserción del primer elemento (mediana es ese elemento)."""
        self.monticulo.insertar(10)
        
        # Debe estar en el montículo Minimo por la lógica de inserción inicial
        self.assertEqual(self.monticulo.valor_mediana, 10)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_max.tamanoActual, 0)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_min.tamanoActual, 1)

    def test_insertar_dos_elementos(self):
        """Prueba un número par de elementos (mediana es el promedio)."""
        self.monticulo.insertar(10) 
        self.monticulo.insertar(20) 
        
        # Mediana esperada: (10 + 20) / 2 = 15.0
        self.assertEqual(self.monticulo.valor_mediana, 15.0)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_max.tamanoActual, 1)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_min.tamanoActual, 1)

    def test_insertar_tres_elementos_impar(self):
        """Prueba un número impar de elementos (mediana es el elemento central)."""
        self.monticulo.insertar(10) # Max: [10]
        self.monticulo.insertar(20) # Min: [20], Max: [10]. Mediana: 15.0
        self.monticulo.insertar(5)  # Max: [10, 5], Min: [20]. Balanceo.
        
        # Mediana esperada: 10 (el mayor de la mitad inferior, o el menor de la mitad superior si balanceado al revés)
        self.assertEqual(self.monticulo.valor_mediana, 10)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_max.tamanoActual, 2)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_min.tamanoActual, 1)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_max.listaMonticulo[1], 10)
        
    def test_balanceo_de_monticulos_MinHeap_crece(self):
        """Verifica el balanceo cuando el Montículo Minimo crece demasiado."""
        self.monticulo.insertar(10) # Mediana: 10
        self.monticulo.insertar(20) # Mediana: 15.0
        self.monticulo.insertar(30) # Min: [20, 30]. Balanceo: 20 se mueve a Max.
        self.monticulo.insertar(40) # Min: [30, 40]. Balanceo: 30 se mueve a Max.
        
        # Estado final después de [10, 20, 30, 40]:
        # MaxHeap (inferior): [20, 10]
        # MinHeap (superior): [40, 30]
        # Mediana esperada: (20 + 30) / 2 = 25.0
        
        self.assertEqual(self.monticulo.valor_mediana, 25.0)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_max.tamanoActual, 2)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_min.tamanoActual, 2)

    def test_balanceo_de_monticulos_MaxHeap_crece(self):
        """Verifica el balanceo cuando el Montículo Maximo crece demasiado."""
        self.monticulo.insertar(10) # Max: [10]
        self.monticulo.insertar(5)  # Max: [10, 5]. Mediana: 7.5
        self.monticulo.insertar(1)  # Max: [10, 5, 1]. Balanceo: 10 se mueve a Min.
        
        # Estado después de [10, 5, 1]:
        # MaxHeap (inferior): [5, 1]
        # MinHeap (superior): [10]
        # Mediana esperada: 5
        self.assertEqual(self.monticulo.valor_mediana, 5)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_max.tamanoActual, 2)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_min.tamanoActual, 1)

    def test_construir_monticulo(self):
        """Verifica el funcionamiento con una lista predefinida."""
        datos_impar = [1, 8, 2, 5, 3] # Ordenado: 1, 2, 3, 5, 8. Mediana: 3
        
        self.monticulo.construir_monticulo(datos_impar)
        
        self.assertEqual(self.monticulo.valor_mediana, 3)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_max.tamanoActual, 3)
        self.assertEqual(self.monticulo._MonticuloMedianaBinario__monticulo_min.tamanoActual, 2)

        # Prueba con lista par
        monticulo_par = MonticuloMedianaBinario()
        datos_par = [1, 8, 2, 5] # Ordenado: 1, 2, 5, 8. Mediana: (2+5)/2 = 3.5
        monticulo_par.construir_monticulo(datos_par)
        
        self.assertEqual(monticulo_par.valor_mediana, 3.5)
        self.assertEqual(monticulo_par._MonticuloMedianaBinario__monticulo_max.tamanoActual, 2)
        self.assertEqual(monticulo_par._MonticuloMedianaBinario__monticulo_min.tamanoActual, 2)

if __name__ == '__main__':
    # Este bloque permite ejecutar las pruebas directamente
    unittest.main()