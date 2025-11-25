import unittest
from unittest.mock import Mock, MagicMock, patch, MagicMock
import sys
from datetime import datetime

# Mock de las dependencias pesadas ANTES de importar los módulos
sys.modules['sklearn'] = MagicMock()
sys.modules['sklearn.feature_extraction'] = MagicMock()
sys.modules['sklearn.feature_extraction.text'] = MagicMock()
sys.modules['sklearn.metrics'] = MagicMock()
sys.modules['sklearn.metrics.pairwise'] = MagicMock()
sys.modules['spacy'] = MagicMock()

from modules.gestores.gestor_usuario import GestorDeUsuarios
from modules.gestores.gestor_reclamo import GestorDeReclamo
from modules.gestores.gestor_dashboard import GestorDashboard
from modules.dominio.usuario import UsuarioFinal
from modules.dominio.reclamo import ReclamoDominio, Estado
from modules.gestores.dashboardService import DashboardService
from modules.reporte.reporteABS import ReporteABS


class TestGestorDeUsuarios(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.mock_repo = Mock()
        self.gestor = GestorDeUsuarios(self.mock_repo)
    
    def test_crear_usuario_exitoso(self):
        """Verifica que se cree un usuario exitosamente"""
        # Configurar mock
        self.mock_repo.obtener_registro_por_filtro.return_value = None
        usuario_creado = UsuarioFinal(
            id=1,
            nombre="Juan",
            apellido="Perez",
            email="juan@example.com",
            usuario="juanp",
            claustro="ESTUDIANTE",
            password="pass123"
        )
        self.mock_repo.obtener_registro_por_filtro.side_effect = [None, None, usuario_creado]
        
        # Ejecutar
        resultado = self.gestor.crear_usuario(
            "Juan", "Perez", "juan@example.com", "juanp", "pass123", "ESTUDIANTE"
        )
        
        # Verificar
        self.assertIsNotNone(resultado)
        self.mock_repo.guardar_registro.assert_called_once()
    
    def test_crear_usuario_email_duplicado(self):
        """Verifica que no se permita crear un usuario con email duplicado"""
        usuario_existente = UsuarioFinal(
            id=1, nombre="Juan", apellido="Perez", 
            email="juan@example.com", usuario="juanp",
            claustro="ESTUDIANTE", password="pass123"
        )
        self.mock_repo.obtener_registro_por_filtro.return_value = usuario_existente
        
        with self.assertRaises(ValueError) as context:
            self.gestor.crear_usuario(
                "Pedro", "Lopez", "juan@example.com", "pedrol", "pass456", "DOCENTE"
            )
        
        self.assertIn("email ya está registrado", str(context.exception))
    
    def test_crear_usuario_datos_incompletos(self):
        """Verifica que no se permita crear un usuario sin datos obligatorios"""
        with self.assertRaises(ValueError) as context:
            self.gestor.crear_usuario("", "Perez", "juan@example.com", "juanp", "pass123", "ESTUDIANTE")
        
        self.assertIn("Faltan datos obligatorios", str(context.exception))
    
    def test_obtener_usuario_por_email(self):
        """Verifica que se obtenga un usuario por email"""
        usuario_mock = Mock()
        self.mock_repo.obtener_registro_por_filtro.return_value = usuario_mock
        
        resultado = self.gestor.obtener_usuario_por_email("juan@example.com")
        
        self.assertEqual(resultado, usuario_mock)
        self.mock_repo.obtener_registro_por_filtro.assert_called_once_with('email', "juan@example.com")
    
    def test_obtener_usuario_por_id(self):
        """Verifica que se obtenga un usuario por ID"""
        usuario_mock = Mock()
        self.mock_repo.obtener_registro_por_filtro.return_value = usuario_mock
        
        resultado = self.gestor.obtener_usuario_por_id(1)
        
        self.assertEqual(resultado, usuario_mock)
        self.mock_repo.obtener_registro_por_filtro.assert_called_once_with('id', 1)
    
    def test_autenticar_usuario_exitoso(self):
        """Verifica que se autentique correctamente un usuario"""
        usuario_mock = UsuarioFinal(
            id=1, nombre="Juan", apellido="Perez",
            email="juan@example.com", usuario="juanp",
            claustro="ESTUDIANTE", password="pass123"
        )
        self.mock_repo.obtener_registro_por_filtro.return_value = usuario_mock
        
        resultado = self.gestor.autenticar_usuario("juan@example.com", "pass123")
        
        self.assertEqual(resultado, usuario_mock)
    
    def test_autenticar_usuario_password_incorrecta(self):
        """Verifica que falle la autenticación con contraseña incorrecta"""
        usuario_mock = UsuarioFinal(
            id=1, nombre="Juan", apellido="Perez",
            email="juan@example.com", usuario="juanp",
            claustro="ESTUDIANTE", password="pass123"
        )
        self.mock_repo.obtener_registro_por_filtro.return_value = usuario_mock
        
        with self.assertRaises(ValueError) as context:
            self.gestor.autenticar_usuario("juan@example.com", "password_incorrecta")
        
        self.assertIn("Credenciales inválidas", str(context.exception))
    
    def test_autenticar_usuario_no_existe(self):
        """Verifica que falle la autenticación cuando el usuario no existe"""
        self.mock_repo.obtener_registro_por_filtro.return_value = None
        
        with self.assertRaises(ValueError) as context:
            self.gestor.autenticar_usuario("noexiste@example.com", "pass123")
        
        self.assertIn("email no está registrado", str(context.exception))


class TestGestorDeReclamo(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.mock_reclamo_repo = Mock()
        self.mock_usuario_repo = Mock()
        self.mock_adhesion_repo = Mock()
        self.gestor = GestorDeReclamo(
            self.mock_reclamo_repo,
            self.mock_usuario_repo,
            self.mock_adhesion_repo
        )
    
    def test_crear_reclamo_exitoso(self):
        """Verifica que se cree un reclamo exitosamente"""
        reclamo_creado = ReclamoDominio(
            id=1,
            usuario_id=1,
            contenido="Problema en el aula",
            timestamp=datetime.now(),
            estado=Estado.PENDIENTE,
            departamento_id=1
        )
        self.mock_reclamo_repo.guardar_registro.return_value = reclamo_creado
        
        resultado = self.gestor.crear_reclamo(
            usuario_id=1,
            contenido="Problema en el aula",
            timestamp=datetime.now(),
            estado=Estado.PENDIENTE,
            departamento_id=1
        )
        
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 1)
        self.mock_reclamo_repo.guardar_registro.assert_called_once()
    
    def test_crear_reclamo_datos_incompletos(self):
        """Verifica que no se permita crear un reclamo sin datos obligatorios"""
        with self.assertRaises(ValueError) as context:
            self.gestor.crear_reclamo(
                usuario_id=None,
                contenido="Problema",
                timestamp=datetime.now(),
                estado=Estado.PENDIENTE
            )
        
        self.assertIn("Todos los campos son obligatorios", str(context.exception))
    
    def test_adherir_usuario_a_reclamo_exitoso(self):
        """Verifica que se adhiera un usuario a un reclamo exitosamente"""
        usuario_mock = Mock()
        self.mock_usuario_repo.obtener_registro_por_filtro.return_value = usuario_mock
        
        self.gestor.adherir_usuario_a_reclamo(2, 1)
        
        self.mock_adhesion_repo.guardar_registro.assert_called_once()
    
    def test_adherir_usuario_no_existe(self):
        """Verifica que no se permita adherir un usuario que no existe"""
        self.mock_usuario_repo.obtener_registro_por_filtro.return_value = None
        
        with self.assertRaises(ValueError) as context:
            self.gestor.adherir_usuario_a_reclamo(999, 1)
        
        self.assertIn("usuario no existe", str(context.exception))
    
    def test_obtener_reclamo_por_id(self):
        """Verifica que se obtenga un reclamo por ID"""
        reclamo_mock = Mock()
        self.mock_reclamo_repo.obtener_registro_por_filtro.return_value = reclamo_mock
        
        resultado = self.gestor.obtener_reclamo_por_id(1)
        
        self.assertEqual(resultado, reclamo_mock)
        self.mock_reclamo_repo.obtener_registro_por_filtro.assert_called_once_with('id', 1)
    
    def test_modificar_estado_reclamo(self):
        """Verifica que se modifique el estado de un reclamo"""
        reclamo_mock = ReclamoDominio(
            id=1,
            usuario_id=1,
            contenido="Problema",
            timestamp=datetime.now(),
            estado=Estado.PENDIENTE,
            departamento_id=1
        )
        self.mock_reclamo_repo.obtener_registro_por_filtro.return_value = reclamo_mock
        self.mock_reclamo_repo.modificar_registro.return_value = reclamo_mock
        
        resultado = self.gestor.modificar_estado_reclamo(1, Estado.EN_PROCESO)
        
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.estado, Estado.EN_PROCESO)
        self.mock_reclamo_repo.modificar_registro.assert_called_once()
    
    def test_modificar_estado_reclamo_no_existe(self):
        """Verifica que retorne None si el reclamo no existe"""
        self.mock_reclamo_repo.obtener_registro_por_filtro.return_value = None
        
        resultado = self.gestor.modificar_estado_reclamo(999, Estado.EN_PROCESO)
        
        self.assertIsNone(resultado)
    
    def test_obtener_todos_los_reclamos(self):
        """Verifica que se obtengan todos los reclamos"""
        reclamos_mock = [Mock(), Mock(), Mock()]
        self.mock_reclamo_repo.obtener_todos_los_registros.return_value = reclamos_mock
        
        resultado = self.gestor.obtener_todos_los_reclamos()
        
        self.assertEqual(len(resultado), 3)
        self.mock_reclamo_repo.obtener_todos_los_registros.assert_called_once()
    
    def test_obtener_reclamos_por_estado(self):
        """Verifica que se obtengan reclamos por estado"""
        reclamos_mock = [Mock(), Mock()]
        self.mock_reclamo_repo.obtener_registros_por_filtro.return_value = reclamos_mock
        
        resultado = self.gestor.obtener_reclamos_por_estado(Estado.PENDIENTE)
        
        self.assertEqual(len(resultado), 2)
        self.mock_reclamo_repo.obtener_registros_por_filtro.assert_called_once_with('estado', Estado.PENDIENTE)


class TestClasificadorReclamos(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.mock_reclamo_repo = Mock()
        self.mock_usuario_repo = Mock()
        self.mock_adhesion_repo = Mock()
        self.gestor = GestorDeReclamo(
            self.mock_reclamo_repo,
            self.mock_usuario_repo,
            self.mock_adhesion_repo
        )
    
    def test_clasificar_reclamo_soporte(self):
        """Verifica que se clasifique correctamente un reclamo de soporte"""
        mock_clasificador = Mock()
        mock_clasificador.classify.return_value = ["soporte informático"]
        
        resultado = self.gestor.clasificar_reclamo("La computadora no enciende", mock_clasificador)
        
        self.assertEqual(resultado, 2)
        mock_clasificador.classify.assert_called_once_with(["La computadora no enciende"])
    
    def test_clasificar_reclamo_maestranza(self):
        """Verifica que se clasifique correctamente un reclamo de maestranza"""
        mock_clasificador = Mock()
        mock_clasificador.classify.return_value = ["maestranza"]
        
        resultado = self.gestor.clasificar_reclamo("El piso está sucio", mock_clasificador)
        
        self.assertEqual(resultado, 1)
    
    def test_clasificar_reclamo_secretaria(self):
        """Verifica que se clasifique correctamente un reclamo de secretaría"""
        mock_clasificador = Mock()
        mock_clasificador.classify.return_value = ["secretaría técnica"]
        
        resultado = self.gestor.clasificar_reclamo("Necesito un certificado", mock_clasificador)
        
        self.assertEqual(resultado, 3)

class TestGestorDashboardSimple(unittest.TestCase):
    
    def setUp(self):
        """Inicializa el GestorDashboard con un mock para DashboardService."""
        self.mock_dashboard_service = Mock(spec=DashboardService)
        self.gestor = GestorDashboard(self.mock_dashboard_service)
        
        # Datos de ejemplo que simulan el retorno de obtener_analiticas
        self.mock_analiticas_data = {
            'datos_torta': {'resuelto': 50.0, 'pendiente': 30.0},
            'datos_nube_palabras': [('problema', 10)],
            'mediana_en_proceso': 100, 
            'mediana_resolucion': 200,
            'mediana_pendiente': 50 
        }
        
        # Configurar el retorno del mock para obtener_analiticas
        self.mock_dashboard_service.obtener_analiticas.return_value = self.mock_analiticas_data

    def test_generar_grafico_torta(self):
        """Verifica que se obtienen los datos y se llama a crear_grafico_torta."""
        id_dep, id_user = 2, 20
        
        # Usamos patch como gestor de contexto para simular la función externa
        with patch('modules.gestores.gestor_dashboard.crear_grafico_torta') as mock_torta:
            self.gestor.generar_grafico_torta(id_dep, id_user)
            
            # 1. Verifica la llamada al servicio para obtener datos
            self.mock_dashboard_service.obtener_analiticas.assert_called_once_with(id_dep, id_user)
            # 2. Verifica la llamada a la función externa con los datos correctos
            mock_torta.assert_called_once_with(self.mock_analiticas_data['datos_torta'])
        
    def test_generar_imagen_nube_palabras(self):
        """Verifica que se obtienen los datos y se llama a crear_imagen_nube_palabras."""
        id_dep, id_user = 3, 30
        
        with patch('modules.gestores.gestor_dashboard.crear_imagen_nube_palabras') as mock_nube:
            self.gestor.generar_imagen_nube_palabras(id_dep, id_user)
            
            self.mock_dashboard_service.obtener_analiticas.assert_called_once_with(id_dep, id_user)
            mock_nube.assert_called_once_with(self.mock_analiticas_data['datos_nube_palabras'])

    def test_generar_barra_mediana(self):
        """Verifica que se obtienen los datos y se llama a crear_barra_mediana."""
        id_dep, id_user = 4, 40
        
        with patch('modules.gestores.gestor_dashboard.crear_barra_mediana') as mock_barra:
            self.gestor.generar_barra_mediana(id_dep, id_user)
            
            self.mock_dashboard_service.obtener_analiticas.assert_called_once_with(id_dep, id_user)
            mock_barra.assert_called_once_with(
                self.mock_analiticas_data['mediana_en_proceso'], 
                self.mock_analiticas_data['mediana_resolucion'],
                self.mock_analiticas_data['mediana_pendiente']
            )
            
    def test_generar_reporte_flujo_completo(self):
        """Verifica la orquestación de la generación de gráficos y la llamada al reporte."""
        id_dep, id_user = 5, 50
        mock_reporte = MagicMock(spec=ReporteABS)
        
        # Patchear las 3 funciones de graficación a la vez
        with patch('modules.gestores.gestor_dashboard.crear_grafico_torta', return_value="Torta") as mock_torta, \
             patch('modules.gestores.gestor_dashboard.crear_imagen_nube_palabras', return_value="Nube") as mock_nube, \
             patch('modules.gestores.gestor_dashboard.crear_barra_mediana', return_value="Barra") as mock_barra:
            
            self.gestor.generar_reporte(mock_reporte, id_dep, id_user)
            
            # 1. Verificar que se llamó a obtener_analiticas 3 veces
            self.assertEqual(self.mock_dashboard_service.obtener_analiticas.call_count, 3)
            
            # 2. Verificar que ReporteABS.generar_reporte fue llamado con las figuras
            mock_reporte.generar_reporte.assert_called_once_with({
                'figura_torta': "Torta",
                'figura_nube_palabras': "Nube",
                'figura_barra_mediana': "Barra"
            })

    

if __name__ == '__main__':
    unittest.main()