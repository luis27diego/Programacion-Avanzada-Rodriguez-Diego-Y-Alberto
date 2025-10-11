from enum import Enum
from datetime import datetime
#from modules.dominio.usuario import UsuarioDominio

class Estado(Enum):
    INVALIDO = 'invalido'
    PENDIENTE = 'pendiente'
    EN_PROCESO = 'en_proceso'
    RESUELTO = 'resuelto'

class ReclamoDominio:
    def __init__(self, usuario_id: int, contenido: str, timestamp: datetime, estado: Estado, id: int = None, departamento_id: int = None, timestamp_modificacion: datetime | None = None):
        self.id = id
        self.usuario_id = usuario_id
        self.contenido = contenido
        self.timestamp = timestamp
        self.estado = estado
        self.departamento_id = departamento_id
        self.timestamp_modificacion = timestamp_modificacion
        self._creador = None
        self._adherentes = []

    def asignar_creador(self, creador):
        if self._creador is not None:
            raise ValueError("Creador ya asignado")
        if creador.id != self.usuario_id:
            raise ValueError("El usuario no coincide con el creador del reclamo")
        self._creador = creador

    def agregar_adherente(self, adherente):
        if adherente.id == self.usuario_id:
            raise ValueError("El creador no puede ser adherente")
        if any(a.id == adherente.id for a in self._adherentes):
            raise ValueError("Adherente ya agregado")
        self._adherentes.append(adherente)

    def obtener_creador(self):
        return self._creador

    def obtener_adherentes(self):
        return self._adherentes[:]

    def cambiar_estado(self, nuevo_estado: Estado, timestamp_modificacion: datetime | None = None):
        if nuevo_estado == Estado.EN_PROCESO and timestamp_modificacion is None:
            raise ValueError("Tiempo de resolución requerido para 'en_proceso'")
        if timestamp_modificacion is not None and not (1 <= timestamp_modificacion <= 15):
            raise ValueError("El tiempo de resolución debe ser entre 1 y 15 días")
        self.estado = nuevo_estado
        self.timestamp_modificacion = timestamp_modificacion

    def cantidad_adherentes(self) -> int:
        return len(self._adherentes)
    
    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "contenido": self.contenido,
            "timestamp": self.timestamp if self.timestamp else None,
            "timestamp_modificacion": self.timestamp_modificacion if self.timestamp_modificacion else None,
            "estado": self.estado.name if hasattr(self.estado, 'name') else self.estado,
            "departamento_id": self.departamento_id,
            "adherentes_id": [a.id for a in self._adherentes],
        }