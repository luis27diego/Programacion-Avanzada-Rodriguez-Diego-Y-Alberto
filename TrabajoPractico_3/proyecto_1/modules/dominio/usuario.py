from enum import Enum
from modules.dominio.reclamo import ReclamoDominio

class Rol(Enum):
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
    RESUELTO = 'resuelto'

class UsuarioDominio:
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
        return self.rol == Rol.SECRETARIO_TECNICO
    
"""     def cambiar_estado(self, reclamo: ReclamoDominio, nuevo_estado: Estado, tiempo_resolucion: int | None = None):
        if not (self.es_jefe() or self.es_secretario()):
            raise PermissionError("Solo jefes o secretario pueden cambiar estados")
        reclamo.cambiar_estado(nuevo_estado, tiempo_resolucion) """