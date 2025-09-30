import unittest
from unittest.mock import MagicMock
from modules.ControladorSistema import ControladorSistema
from modules.CintaTransportadora import DetectorAlimento

class TestControladorSistema(unittest.TestCase):
    def setUp(self):
        """Configura el entorno para cada prueba"""
        self.controlador = ControladorSistema()
        self.controlador.cinta = MagicMock(spec=DetectorAlimento)

    def test_iniciar_proceso(self):
        """Prueba la inicialización del proceso con un nuevo cajón"""
        capacidad = 5
        result = self.controlador.iniciar_proceso(capacidad)
        
        self.assertTrue(result)
        self.assertEqual(self.controlador.estado, "running")
        self.assertEqual(self.controlador.cajon_actual.capacidad_maxima, capacidad)
        self.assertEqual(self.controlador.alimentos_procesados, 0)
        self.assertEqual(self.controlador.alimentos_desviados, 0)

    def test_procesar_siguiente_alimento_exitoso(self):
        """Prueba procesar un alimento correctamente"""
        self.controlador.iniciar_proceso(5)
        deteccion = {"alimento": "manzana", "peso": 0.15}
        self.controlador.cinta.detectar_alimento.return_value = deteccion
        
        mock_alimento = MagicMock()
        mock_alimento.calcular_aw.return_value = 0.81
        with unittest.mock.patch('modules.Crear_alimento.crear_alimento', return_value=mock_alimento):
            result = self.controlador.procesar_siguiente_alimento()
            print(result)
        
        self.assertEqual(result["tipo"], "agregado")
        self.assertEqual(result["alimento"], "manzana")
        self.assertEqual(result["peso"], 0.15)
        self.assertAlmostEqual(result["aw"], 0.81, places=2)
        self.assertEqual(self.controlador.alimentos_procesados, 1)

    def test_procesar_siguiente_alimento_falla_deteccion(self):
        """Prueba procesar alimento con detección fallida"""
        self.controlador.iniciar_proceso(5)
        self.controlador.cinta.detectar_alimento.return_value = "undefined"
        
        result = self.controlador.procesar_siguiente_alimento()
        
        self.assertEqual(result["tipo"], "desviado")
        self.assertEqual(self.controlador.alimentos_desviados, 1)
        self.assertEqual(self.controlador.alimentos_procesados, 0)

    def test_obtener_estado_actual(self):
        """Prueba obtener el estado actual del sistema"""
        self.controlador.iniciar_proceso(5)
        # Simular 2 alimentos en el cajón
        mock_alimento1 = MagicMock()
        mock_alimento2 = MagicMock()
        self.controlador.cajon_actual._alimentos = [mock_alimento1, mock_alimento2]
        # Configurar mocks para métodos del cajón
        self.controlador.cajon_actual.peso_total = MagicMock(return_value=1.0)
        self.controlador.cajon_actual.aw_promedio_total = MagicMock(return_value=0.85)
        self.controlador.cajon_actual.aw_promedio_por_tipo = MagicMock(return_value={
            "aw_prom_frutas": 0.8,
            "aw_prom_verduras": 0.9
        })
        self.controlador.cajon_actual.aw_promedio_por_alimento = MagicMock(return_value={
            "aw_prom_manzana": 0.8,
            "aw_prom_papa": 0.9
        })
        self.controlador.alimentos_procesados = 3
        self.controlador.alimentos_desviados = 1
        
        result = self.controlador.obtener_estado_actual()
        
        self.assertEqual(result["estado"], "running")
        self.assertEqual(result["progreso"]["actual"], 2)  # Basado en len(_alimentos)
        self.assertEqual(result["progreso"]["total"], 5)
        self.assertEqual(result["estadisticas"]["peso_total"], 1.0)
        self.assertEqual(result["estadisticas"]["alimentos_procesados"], 3)
        self.assertEqual(result["estadisticas"]["alimentos_desviados"], 1)

if __name__ == '__main__':
    unittest.main()