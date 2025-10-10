import unittest
from unittest.mock import MagicMock, patch
from modules.ControladorSistema import ControladorSistema
from modules.Cajon import Cajon
from modules.Frutas import Manzana, Kiwi
from modules.Verduras import Papa, Zanahoria

class TestControladorSistema(unittest.TestCase):
    
    def setUp(self):
        """Configura el entorno para cada prueba"""
        self.controlador = ControladorSistema()
        self.controlador.cinta = MagicMock()

    def test_iniciar_proceso(self):
        """Prueba la inicialización del proceso con un nuevo cajón"""
        self.controlador.iniciar_proceso(capacidad_cajon=5)
        
        self.assertEqual(self.controlador.estado, "running")
        self.assertEqual(self.controlador.cajon_actual.capacidad_maxima, 5)
        self.assertEqual(self.controlador.alimentos_procesados, 0)
        self.assertEqual(self.controlador.alimentos_desviados, 0)

    @patch('modules.Crear_alimento.crear_alimento')
    def test_procesar_hasta_llenar(self, mock_crear_alimento):
        """Prueba el procesamiento hasta llenar el cajón"""
        # Configurar estado inicial
        self.controlador.iniciar_proceso(capacidad_cajon=10)
        
        # Simular cajón que se llena después de 3 iteraciones
        self.controlador.cajon_actual.esta_lleno = MagicMock(
            side_effect=[False, False, False, True]
        )
        self.controlador.cajon_actual.agregar_alimento = MagicMock()
        
        # Simular detecciones: 2 exitosas, 1 fallida
        self.controlador.cinta.detectar_alimento.side_effect = [
            {"alimento": "manzana", "peso": 0.5},
            "undefined",
            {"alimento": "kiwi", "peso": 0.08}
        ]
        
        # Mock del alimento creado
        mock_crear_alimento.return_value = MagicMock()
        
        # Ejecutar
        self.controlador.procesar_hasta_llenar()
        
        # Verificar resultados
        self.assertEqual(self.controlador.estado, "complete")
        self.assertEqual(self.controlador.alimentos_procesados, 2)
        self.assertEqual(self.controlador.alimentos_desviados, 1)
        self.assertEqual(self.controlador.cajon_actual.agregar_alimento.call_count, 2)
        
    def test_obtener_estado_actual(self):
        """Debe retornar estadísticas y advertencias correctas con cajón lleno"""
        # Crear y asignar un cajón con capacidad 3
        cajon = Cajon(3)
        cajon.agregar_alimento(Manzana(0.2))
        cajon.agregar_alimento(Kiwi(0.5))
        cajon.agregar_alimento(Papa(0.3))

        # Asignarlo al controlador
        self.controlador.cajon_actual = cajon
        self.controlador.estado = "complete"
        self.controlador.alimentos_procesados = 3
        self.controlador.alimentos_desviados = 1
        
        resultado = self.controlador.obtener_estado_actual()

        # Verificar estructura general
        self.assertEqual(resultado["estado"], "complete")
        self.assertIn("estadisticas", resultado)
        self.assertIn("advertencias", resultado)

        # Verificar progreso
        progreso = resultado["progreso"]
        self.assertEqual(progreso["actual"], 3)
        self.assertEqual(progreso["total"], 3)

        # Verificar estadísticas esperadas
        estadisticas = resultado["estadisticas"]
        self.assertIn("peso_total", estadisticas)
        self.assertIn("aw_total", estadisticas)
        self.assertEqual(estadisticas["alimentos_procesados"], 3)
        self.assertEqual(estadisticas["alimentos_desviados"], 1)

        # Las advertencias podrían estar vacías o no, dependiendo del aw
        self.assertIsInstance(resultado["advertencias"], list)

if __name__ == '__main__':
    unittest.main()