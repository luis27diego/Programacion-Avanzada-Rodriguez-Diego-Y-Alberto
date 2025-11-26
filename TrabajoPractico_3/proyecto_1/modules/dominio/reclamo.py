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
        self.__usuario_id = usuario_id
        self.__contenido = contenido
        self.__timestamp = timestamp
        self.__estado = estado
        self.__departamento_id = departamento_id
        self.__timestamp_modificacion = timestamp_modificacion
        self.__adherentes = []

    @property
    def usuario_id(self):
        return self.__usuario_id
    @property
    def contenido(self):
        return self.__contenido
    @property
    def timestamp(self):
        return self.__timestamp
    @property
    def timestamp_modificacion(self):
        return self.__timestamp_modificacion
    @property
    def estado(self):
        return self.__estado
    @property
    def departamento_id(self):
        return self.__departamento_id
    
    @estado.setter
    def estado(self, nuevo_estado: Estado):
        self.__estado = nuevo_estado

    @timestamp_modificacion.setter
    def timestamp_modificacion(self, nuevo_timestamp: datetime):
        if not isinstance(nuevo_timestamp, datetime):
            raise ValueError("timestamp_modificacion debe ser un objeto datetime")
        self.__timestamp_modificacion = nuevo_timestamp
        
    @departamento_id.setter
    def departamento_id(self, nuevo_departamento_id: int):
        self.__departamento_id = nuevo_departamento_id

    def agregar_adherente(self, adherente):
        if adherente== self.usuario_id:
            raise ValueError("El creador no puede ser adherente")
        if any(a == adherente for a in self.__adherentes):
            raise ValueError("Adherente ya agregado")
        self.__adherentes.append(adherente)

    def obtener_creador(self):
        return self.usuario_id

    def obtener_adherentes(self):
        return self.__adherentes[:]

    def cantidad_adherentes(self) -> int:
        return len(self.__adherentes)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "contenido": self.contenido,
            "timestamp": self.timestamp if self.timestamp else None,
            "timestamp_modificacion": self.timestamp_modificacion if self.timestamp_modificacion else None,
            "estado": self.estado.name if hasattr(self.estado, 'name') else self.estado,
            "departamento_id": self.departamento_id,
            "adherentes_id": [a for a in self.__adherentes],
        }
class AdhesionDominio:
    def __init__(self, usuario_id: int, reclamo_id: int, id: int = None):
        self.id = id
        self.usuario_id = usuario_id
        self.reclamo_id = reclamo_id
