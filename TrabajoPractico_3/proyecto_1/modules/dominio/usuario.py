from enum import Enum
from modules.dominio.reclamo import ReclamoDominio
from abc import ABC

""" class Rol(Enum):
    USUARIO_FINAL = 'usuario_final'
    JEFE_DEPARTAMENTO = 'jefe_departamento'
    SECRETARIO_TECNICO = 'secretario_tecnico'

class Claustro(Enum):
    ESTUDIANTE = 'estudiante'
    DOCENTE = 'docente'
    PAYS = 'PAyS'

class Estado(Enum):
    INVALIDO = 'invalido'
    PENDIENTE = 'pendiente'
    EN_PROCESO = 'en_proceso'
    RESUELTO = 'resuelto' """
class UsuarioDominio(ABC):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, 
                 password: str, id: int = None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.usuario = usuario
        self.password = password
""" class UsuarioDominio:
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, 
                 claustro: Claustro | None, password: str, rol: Rol, id: int = None, departamento_id: int | None = None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.usuario = usuario
        self.claustro = claustro
        self.password = password
        self.rol = rol
        self.departamento_id = departamento_id
        self._reclamos_creados = []
        self._reclamos_adheridos = []

    def agregar_reclamo_creado(self, reclamo: 'ReclamoDominio'):
        if reclamo.usuario_id != self.id:
            raise ValueError("El reclamo no fue creado por este usuario")
        if any(r.id == reclamo.id for r in self._reclamos_creados):
            raise ValueError("Reclamo ya agregado")
        self._reclamos_creados.append(reclamo)

    def agregar_reclamo_adherido(self, reclamo: 'ReclamoDominio'):
        if reclamo.usuario_id == self.id:
            raise ValueError("No se puede adherir a un reclamo propio")
        if any(r.id == reclamo.id for r in self._reclamos_adheridos):
            raise ValueError("Ya adherido a este reclamo")
        self._reclamos_adheridos.append(reclamo)

    def obtener_reclamos_creados(self) -> list['ReclamoDominio']:
        return self._reclamos_creados[:]

    def obtener_reclamos_adheridos(self) -> list['ReclamoDominio']:
        return self._reclamos_adheridos[:]

    def es_jefe(self) -> bool:
        return self.rol == Rol.JEFE_DEPARTAMENTO

    def es_secretario(self) -> bool:
        return self.rol == Rol.SECRETARIO_TECNICO """
    
"""     def cambiar_estado(self, reclamo: ReclamoDominio, nuevo_estado: Estado, tiempo_resolucion: int | None = None):
        if not (self.es_jefe() or self.es_secretario()):
            raise PermissionError("Solo jefes o secretario pueden cambiar estados")
        reclamo.cambiar_estado(nuevo_estado, tiempo_resolucion) """
class UsuarioFinal(UsuarioDominio):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, 
                 claustro: str, password: str, id: int = None):
        super().__init__(nombre, apellido, email, usuario, password, id)
        self.claustro = claustro
        self._reclamos_creados = []
        self._reclamos_adheridos = []
        
    def agregar_reclamo_creado(self, reclamo: int):
        if any(r == reclamo for r in self._reclamos_creados):
            raise ValueError("Reclamo ya agregado")
        self._reclamos_creados.append(reclamo)

    def agregar_reclamo_adherido(self, reclamo: int):
        if any(r == reclamo for r in self._reclamos_adheridos):
            raise ValueError("Ya adherido a este reclamo")
        self._reclamos_adheridos.append(reclamo)

    def obtener_reclamos_creados(self) -> list['ReclamoDominio']:
        return self._reclamos_creados[:]

    def obtener_reclamos_adheridos(self) -> list['ReclamoDominio']:
        return self._reclamos_adheridos[:]

class ResponsableDepartamento(UsuarioDominio):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, 
                 password: str, rol: str, id: int = None, departamento_id: int = None):

        super().__init__(nombre, apellido, email, usuario, password, id)
        self.rol = rol
        self.departamento_id = departamento_id

if __name__ == "__main__":
    usuario = UsuarioFinal(
        nombre="Juan",
        apellido="Perez",
        email="juan.perez@example.com",
        usuario="juanp",
        claustro='estudiante',
        password="password123"
    )
    print(f"Usuario creado: {usuario.nombre} {usuario.apellido}, Claustro: {usuario.claustro}")

    responsable = ResponsableDepartamento(
        nombre="Ana",
        apellido="Gomez",
        email="ana.gomez@example.com",
        usuario="anag",
        password="password456",
        rol='jefe_departamento',
        departamento_id=1
    )
    print(f"Responsable creado: {responsable.nombre} {responsable.apellido}, Rol: {responsable.rol}, Departamento ID: {responsable.departamento_id}")

    responsable_secretario = ResponsableDepartamento(
        nombre="Luis",
        apellido="Martinez",
        email="luis.martinez@example.com",
        usuario="luism",
        password="password789",
        rol='secretario_tecnico',
        departamento_id=1
    )
    print(f"Responsable creado: {responsable_secretario.nombre} {responsable_secretario.apellido}, Rol: {responsable_secretario.rol}, Departamento ID: {responsable_secretario.departamento_id}")