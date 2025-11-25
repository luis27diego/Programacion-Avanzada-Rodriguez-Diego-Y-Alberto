import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from modules.repositorioConcreto.usuario_concreto import UsuarioRepositorio
from modules.repositorioConcreto.reclamo_concreto import ReclamoRepositorio
from modules.repositorioConcreto.departamento_concreto import DepartamentoRepositorio
from modules.repositorioConcreto.adhesion_concreto import AdhesionRepositorio
from modules.dominio.usuario import UsuarioFinal, ResponsableDepartamento
from modules.dominio.reclamo import ReclamoDominio, Estado, AdhesionDominio
from modules.dominio.departamento import DepartamentoDominio
from modules.modelos.usuarioModel import UsuarioModel
from modules.modelos.reclamoModel import ReclamoModel
from modules.modelos.departamentoModel import DepartamentoModel
from modules.modelos.adhesionModel import AdhesionModel


class TestUsuarioRepositorio(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.mock_session = Mock()
        self.repositorio = UsuarioRepositorio(self.mock_session)
    
    def test_guardar_registro_usuario_final(self):
        """Verifica que se guarde un usuario final correctamente"""
        usuario = UsuarioFinal(
            id=None,
            nombre="Juan",
            apellido="Perez",
            email="juan@example.com",
            usuario="juanp",
            claustro="ESTUDIANTE",
            password="pass123"
        )
        
        self.repositorio.guardar_registro(usuario)
        
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
    
    def test_guardar_registro_responsable(self):
        """Verifica que se guarde un responsable correctamente"""
        responsable = ResponsableDepartamento(
            id=None,
            nombre="Ana",
            apellido="Gomez",
            email="ana@example.com",
            usuario="anag",
            password="pass456",
            rol="JEFE_DEPARTAMENTO",
            departamento_id=1
        )
        
        self.repositorio.guardar_registro(responsable)
        
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
    
    def test_obtener_registro_por_filtro_email(self):
        """Verifica que se obtenga un usuario por email"""
        mock_query = Mock()
        mock_usuario_modelo = UsuarioModel(
            id=1,
            nombre="Juan",
            apellido="Perez",
            email="juan@example.com",
            usuario="juanp",
            claustro="ESTUDIANTE",
            password="pass123",
            rol=None,
            departamento_id=None
        )
        
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value.first.return_value = mock_usuario_modelo
        mock_query.filter.return_value.all.return_value = []
        
        # Mock para las consultas adicionales de reclamos
        self.mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = []
        
        resultado = self.repositorio.obtener_registro_por_filtro('email', 'juan@example.com')
        
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.email, 'juan@example.com')
    
    def test_obtener_registro_por_filtro_no_existe(self):
        """Verifica que retorne None si el usuario no existe"""
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value.first.return_value = None
        
        resultado = self.repositorio.obtener_registro_por_filtro('email', 'noexiste@example.com')
        
        self.assertIsNone(resultado)
    
    def test_modificar_registro(self):
        """Verifica que se modifique un usuario correctamente"""
        usuario_modificado = UsuarioFinal(
            id=1,
            nombre="Juan Modificado",
            apellido="Perez",
            email="juan@example.com",
            usuario="juanp",
            claustro="DOCENTE",
            password="pass123"
        )
        
        mock_usuario_modelo = Mock()
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value.first.return_value = mock_usuario_modelo
        
        self.repositorio.modificar_registro(usuario_modificado)
        
        self.assertEqual(mock_usuario_modelo.nombre, "Juan Modificado")
        self.assertEqual(mock_usuario_modelo.claustro, "DOCENTE")
        self.mock_session.commit.assert_called()
    
    def test_eliminar_registro(self):
        """Verifica que se elimine un usuario correctamente"""
        mock_usuario = Mock()
        self.mock_session.query.return_value.get.return_value = mock_usuario
        
        self.repositorio.eliminar_registro(1)
        
        self.mock_session.delete.assert_called_once_with(mock_usuario)
        self.mock_session.commit.assert_called_once()


class TestReclamoRepositorio(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.mock_session = Mock()
        self.repositorio = ReclamoRepositorio(self.mock_session)
    
    def test_guardar_registro(self):
        """Verifica que se guarde un reclamo correctamente"""
        reclamo = ReclamoDominio(
            id=None,
            usuario_id=1,
            contenido="Problema en el aula",
            timestamp=datetime.now(),
            estado=Estado.PENDIENTE,
            departamento_id=1,
            timestamp_modificacion=datetime.now()
        )
        
        
        self.mock_session.refresh = Mock()
        self.mock_session.add = Mock()
        self.mock_session.commit = Mock()
        

        # Mock para la consulta de adherentes
        self.mock_session.query.return_value.filter.return_value.all.return_value = []
        
        resultado = self.repositorio.guardar_registro(reclamo)
        
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
    
    def test_obtener_registro_por_filtro(self):
        """Verifica que se obtenga un reclamo por filtro"""
        mock_reclamo_modelo = ReclamoModel(
            id=1,
            usuario_id=1,
            contenido="Problema",
            timestamp=datetime.now(),
            estado=Estado.PENDIENTE,
            departamento_id=1
        )
        
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value.first.return_value = mock_reclamo_modelo
        mock_query.filter.return_value.all.return_value = []
        
        resultado = self.repositorio.obtener_registro_por_filtro('id', 1)
        
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 1)
    
    def test_modificar_registro(self):
        """Verifica que se modifique un reclamo correctamente"""
        reclamo = ReclamoDominio(
            id=1,
            usuario_id=1,
            contenido="Problema modificado",
            timestamp=datetime.now(),
            estado=Estado.EN_PROCESO,
            departamento_id=1,
            timestamp_modificacion=datetime.now()
        )
        
        mock_reclamo_modelo = Mock()
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value.first.return_value = mock_reclamo_modelo
        
        self.repositorio.modificar_registro(reclamo)
        
        self.assertEqual(mock_reclamo_modelo.contenido, "Problema modificado")
        self.mock_session.commit.assert_called_once()
    
    def test_eliminar_registro(self):
        """Verifica que se elimine un reclamo correctamente"""
        mock_reclamo = Mock()
        self.mock_session.query.return_value.get.return_value = mock_reclamo
        
        self.repositorio.eliminar_registro(1)
        
        self.mock_session.delete.assert_called_once_with(mock_reclamo)
        self.mock_session.commit.assert_called_once()


class TestDepartamentoRepositorio(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.mock_session = Mock()
        self.repositorio = DepartamentoRepositorio(self.mock_session)
    
    def test_guardar_registro(self):
        """Verifica que se guarde un departamento correctamente"""
        departamento = DepartamentoDominio(id=None, nombre="Soporte Informático")
        
        self.repositorio.guardar_registro(departamento)
        
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
    
    def test_obtener_registro_por_filtro(self):
        """Verifica que se obtenga un departamento por filtro"""
        mock_departamento_modelo = DepartamentoModel(
            id=1,
            nombre="Soporte Informático"
        )
        
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value.first.return_value = mock_departamento_modelo
        
        resultado = self.repositorio.obtener_registro_por_filtro('id', 1)
        
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Soporte Informático")
    
    def test_obtener_todos_los_registros(self):
        """Verifica que se obtengan todos los departamentos"""
        mock_departamentos = [
            DepartamentoModel(id=1, nombre="Soporte"),
            DepartamentoModel(id=2, nombre="Maestranza")
        ]
        
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.all.return_value = mock_departamentos
        
        resultado = self.repositorio.obtener_todos_los_registros()
        
        self.assertEqual(len(resultado), 2)
    
    def test_modificar_registro(self):
        """Verifica que se modifique un departamento correctamente"""
        departamento = DepartamentoDominio(id=1, nombre="Soporte Modificado")
        
        mock_departamento_modelo = Mock()
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value.first.return_value = mock_departamento_modelo
        
        self.repositorio.modificar_registro(departamento)
        
        self.assertEqual(mock_departamento_modelo.nombre, "Soporte Modificado")
        self.mock_session.commit.assert_called()
    
    def test_eliminar_registro(self):
        """Verifica que se elimine un departamento correctamente"""
        mock_departamento = Mock()
        self.mock_session.query.return_value.get.return_value = mock_departamento
        
        self.repositorio.eliminar_registro(1)
        
        self.mock_session.delete.assert_called_once_with(mock_departamento)
        self.mock_session.commit.assert_called_once()


class TestAdhesionRepositorio(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.mock_session = Mock()
        self.repositorio = AdhesionRepositorio(self.mock_session)
    
    def test_guardar_registro(self):
        """Verifica que se guarde una adhesión correctamente"""
        adhesion = AdhesionDominio(id=None, usuario_id=2, reclamo_id=1)
        
        self.repositorio.guardar_registro(adhesion)
        
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
    
    def test_obtener_registro_por_filtro(self):
        """Verifica que se obtenga una adhesión por filtro"""
        mock_adhesion_modelo = AdhesionModel(
            id=1,
            usuario_id=2,
            reclamo_id=1
        )
        
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value.first.return_value = mock_adhesion_modelo
        
        resultado = self.repositorio.obtener_registro_por_filtro('id', 1)
        
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.usuario_id, 2)
        self.assertEqual(resultado.reclamo_id, 1)
    
    def test_obtener_todos_los_registros(self):
        """Verifica que se obtengan todas las adhesiones"""
        mock_adhesiones = [
            AdhesionModel(id=1, usuario_id=2, reclamo_id=1),
            AdhesionModel(id=2, usuario_id=3, reclamo_id=1)
        ]
        
        mock_query = Mock()
        self.mock_session.query.return_value = mock_query
        mock_query.all.return_value = mock_adhesiones
        
        resultado = self.repositorio.obtener_todos_los_registros()
        
        self.assertEqual(len(resultado), 2)
    
    def test_eliminar_registro(self):
        """Verifica que se elimine una adhesión correctamente"""
        mock_adhesion = Mock()
        self.mock_session.query.return_value.get.return_value = mock_adhesion
        
        self.repositorio.eliminar_registro(1)
        
        self.mock_session.delete.assert_called_once_with(mock_adhesion)
        self.mock_session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()