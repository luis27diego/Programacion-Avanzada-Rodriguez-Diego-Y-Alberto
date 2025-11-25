import unittest
from datetime import datetime
from modules.dominio.usuario import UsuarioFinal, ResponsableDepartamento
from modules.dominio.reclamo import ReclamoDominio, Estado, AdhesionDominio
from modules.dominio.departamento import DepartamentoDominio


class TestUsuarioFinal(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.usuario = UsuarioFinal(
            id=1,
            nombre="Juan",
            apellido="Perez",
            email="juan@example.com",
            usuario="juanp",
            claustro="ESTUDIANTE",
            password="pass123"
        )
    
    def test_crear_usuario_final(self):
        """Verifica que se cree correctamente un usuario final"""
        self.assertEqual(self.usuario.id, 1)
        self.assertEqual(self.usuario.nombre, "Juan")
        self.assertEqual(self.usuario.apellido, "Perez")
        self.assertEqual(self.usuario.email, "juan@example.com")
        self.assertEqual(self.usuario.usuario, "juanp")
        self.assertEqual(self.usuario.claustro, "ESTUDIANTE")
        self.assertEqual(self.usuario.password, "pass123")
    
    def test_agregar_reclamo_creado(self):
        """Verifica que se agregue un reclamo creado correctamente"""
        self.usuario.agregar_reclamo_creado(1)
        reclamos = self.usuario.obtener_reclamos_creados()
        self.assertEqual(len(reclamos), 1)
        self.assertIn(1, reclamos)
    
    def test_agregar_reclamo_creado_duplicado(self):
        """Verifica que no se permita agregar un reclamo duplicado"""
        self.usuario.agregar_reclamo_creado(1)
        with self.assertRaises(ValueError):
            self.usuario.agregar_reclamo_creado(1)
    
    def test_agregar_reclamo_adherido(self):
        """Verifica que se agregue un reclamo adherido correctamente"""
        self.usuario.agregar_reclamo_adherido(2)
        reclamos = self.usuario.obtener_reclamos_adheridos()
        self.assertEqual(len(reclamos), 1)
        self.assertIn(2, reclamos)
    
    def test_agregar_reclamo_adherido_duplicado(self):
        """Verifica que no se permita adherir dos veces al mismo reclamo"""
        self.usuario.agregar_reclamo_adherido(2)
        with self.assertRaises(ValueError):
            self.usuario.agregar_reclamo_adherido(2)


class TestResponsableDepartamento(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.responsable = ResponsableDepartamento(
            id=1,
            nombre="Ana",
            apellido="Gomez",
            email="ana@example.com",
            usuario="anag",
            password="pass456",
            rol="JEFE_DEPARTAMENTO",
            departamento_id=1
        )
    
    def test_crear_responsable(self):
        """Verifica que se cree correctamente un responsable"""
        self.assertEqual(self.responsable.id, 1)
        self.assertEqual(self.responsable.rol, "JEFE_DEPARTAMENTO")
        self.assertEqual(self.responsable.departamento_id, 1)
    
    def test_propiedades_responsable(self):
        """Verifica que las propiedades sean accesibles"""
        self.assertEqual(self.responsable.nombre, "Ana")
        self.assertEqual(self.responsable.email, "ana@example.com")


class TestReclamoDominio(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.reclamo = ReclamoDominio(
            id=1,
            usuario_id=1,
            contenido="Problema en el aula 101",
            timestamp=datetime.now(),
            estado=Estado.PENDIENTE,
            departamento_id=1
        )
    
    def test_crear_reclamo(self):
        """Verifica que se cree correctamente un reclamo"""
        self.assertEqual(self.reclamo.id, 1)
        self.assertEqual(self.reclamo.usuario_id, 1)
        self.assertEqual(self.reclamo.contenido, "Problema en el aula 101")
        self.assertEqual(self.reclamo.estado, Estado.PENDIENTE)
        self.assertEqual(self.reclamo.departamento_id, 1)
    
    def test_agregar_adherente(self):
        """Verifica que se agregue un adherente correctamente"""
        self.reclamo.agregar_adherente(2)
        adherentes = self.reclamo.obtener_adherentes()
        self.assertEqual(len(adherentes), 1)
        self.assertIn(2, adherentes)
    
    def test_agregar_adherente_duplicado(self):
        """Verifica que no se permita agregar un adherente duplicado"""
        self.reclamo.agregar_adherente(2)
        with self.assertRaises(ValueError):
            self.reclamo.agregar_adherente(2)
    
    def test_agregar_creador_como_adherente(self):
        """Verifica que el creador no pueda ser adherente"""
        with self.assertRaises(ValueError):
            self.reclamo.agregar_adherente(1)
    
    def test_cantidad_adherentes(self):
        """Verifica que se cuente correctamente la cantidad de adherentes"""
        self.assertEqual(self.reclamo.cantidad_adherentes(), 0)
        self.reclamo.agregar_adherente(2)
        self.assertEqual(self.reclamo.cantidad_adherentes(), 1)
        self.reclamo.agregar_adherente(3)
        self.assertEqual(self.reclamo.cantidad_adherentes(), 2)
    
    def test_modificar_estado(self):
        """Verifica que se pueda modificar el estado del reclamo"""
        self.reclamo.estado = Estado.EN_PROCESO
        self.assertEqual(self.reclamo.estado, Estado.EN_PROCESO)
    
    def test_modificar_timestamp_modificacion(self):
        """Verifica que se pueda modificar el timestamp de modificación"""
        nuevo_timestamp = datetime.now()
        self.reclamo.timestamp_modificacion = nuevo_timestamp
        self.assertEqual(self.reclamo.timestamp_modificacion, nuevo_timestamp)
    
    def test_to_dict(self):
        """Verifica que el método to_dict funcione correctamente"""
        self.reclamo.agregar_adherente(2)
        dict_reclamo = self.reclamo.to_dict()
        self.assertEqual(dict_reclamo['id'], 1)
        self.assertEqual(dict_reclamo['usuario_id'], 1)
        self.assertEqual(dict_reclamo['contenido'], "Problema en el aula 101")
        self.assertIn(2, dict_reclamo['adherentes_id'])


class TestAdhesionDominio(unittest.TestCase):
    
    def test_crear_adhesion(self):
        """Verifica que se cree correctamente una adhesión"""
        adhesion = AdhesionDominio(id=1, usuario_id=2, reclamo_id=3)
        self.assertEqual(adhesion.id, 1)
        self.assertEqual(adhesion.usuario_id, 2)
        self.assertEqual(adhesion.reclamo_id, 3)


class TestDepartamentoDominio(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.departamento = DepartamentoDominio(id=1, nombre="Soporte Informático")
    
    def test_crear_departamento(self):
        """Verifica que se cree correctamente un departamento"""
        self.assertEqual(self.departamento.id, 1)
        self.assertEqual(self.departamento.nombre, "Soporte Informático")
    
    def test_agregar_user_asociado_valido(self):
        """Verifica que se agregue un usuario asociado correctamente"""
        responsable = ResponsableDepartamento(
            id=1,
            nombre="Ana",
            apellido="Gomez",
            email="ana@example.com",
            usuario="anag",
            password="pass456",
            rol="JEFE_DEPARTAMENTO",
            departamento_id=1
        )
        self.departamento.agregar_user_asociado(responsable)
        usuarios = self.departamento.get_users_asociados()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].id, 1)
    
    def test_agregar_user_asociado_invalido(self):
        """Verifica que no se permita agregar un usuario de otro departamento"""
        responsable = ResponsableDepartamento(
            id=1,
            nombre="Ana",
            apellido="Gomez",
            email="ana@example.com",
            usuario="anag",
            password="pass456",
            rol="JEFE_DEPARTAMENTO",
            departamento_id=2  # Departamento diferente
        )
        with self.assertRaises(ValueError):
            self.departamento.agregar_user_asociado(responsable)


if __name__ == '__main__':
    unittest.main()
