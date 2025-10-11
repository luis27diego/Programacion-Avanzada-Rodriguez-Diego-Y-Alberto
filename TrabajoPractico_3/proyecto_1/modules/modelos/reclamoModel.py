from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from . import Base
from sqlalchemy.sql import func
from modules.dominio.reclamo import Estado  # Asumiendo que están en un módulo separado

class ReclamoModel(Base):
    __tablename__ = 'reclamos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False, index=True)
    contenido = Column(String(1000), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=func.now(), index=True)
    estado = Column(Enum(Estado), nullable=False, default=Estado.PENDIENTE)
    departamento_id = Column(Integer, ForeignKey('departamentos.id'), nullable=True, index=True)
    timestamp_modificacion = Column(DateTime, nullable=True, index=True)

    usuario = relationship('UsuarioModel', back_populates='reclamos')
    departamento = relationship('DepartamentoModel', back_populates='reclamos')