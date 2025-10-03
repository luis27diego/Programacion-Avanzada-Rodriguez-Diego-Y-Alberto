import unittest
from unittest.mock import MagicMock, patch
from modules.ControladorSistema import ControladorSistema


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
            {"alimento": "manzana", "peso": 150},
            "undefined",
            {"alimento": "kiwi", "peso": 80}
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
        """Prueba obtener el estado actual del sistema"""
        # Configurar estado y cajón mockeado
        self.controlador.estado = "running"
        self.controlador.alimentos_procesados = 3
        self.controlador.alimentos_desviados = 1
        
        # Mockear el cajón completo
        mock_cajon = MagicMock()
        mock_cajon.cantidad_actual = 2
        mock_cajon.capacidad_maxima = 5
        mock_cajon.peso_total.return_value = 1.0
        mock_cajon.aw_promedio_total.return_value = 0.85
        mock_cajon.aw_promedio_por_tipo.return_value = {
            "aw_prom_frutas": 0.8,
            "aw_prom_verduras": 0.9
        }
        mock_cajon.aw_promedio_por_alimento.return_value = {
            "aw_prom_manzana": 0.8,
            "aw_prom_papa": 0.9
        }
        mock_cajon.obtener_advertencias.return_value = []
        
        self.controlador.cajon_actual = mock_cajon
        
        # Ejecutar
        result = self.controlador.obtener_estado_actual()
        
        # Verificar
        self.assertEqual(result["estado"], "running")
        self.assertEqual(result["progreso"]["actual"], 2)
        self.assertEqual(result["progreso"]["total"], 5)
        self.assertEqual(result["estadisticas"]["peso_total"], 1.0)
        self.assertEqual(result["estadisticas"]["alimentos_procesados"], 3)
        self.assertEqual(result["estadisticas"]["alimentos_desviados"], 1)

if __name__ == '__main__':
    unittest.main()