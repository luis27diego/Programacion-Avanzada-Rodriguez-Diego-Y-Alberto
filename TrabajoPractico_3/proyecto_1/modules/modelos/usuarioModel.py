from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
from modules.dominio.usuario import Rol, Claustro  # Asumiendo que están en un módulo separado
from . import Base

class UsuarioModel(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    usuario = Column(String(50), nullable=False, unique=True, index=True)
    claustro = Column(Enum(Claustro), nullable=True)
    password = Column(String(255), nullable=False)  # Hasheada
    rol = Column(Enum(Rol), nullable=False)
    departamento_id = Column(Integer, ForeignKey('departamentos.id'), nullable=True)

    departamento = relationship('DepartamentoModel', back_populates='usuarios')
    reclamos = relationship('ReclamoModel', back_populates='usuario', foreign_keys='ReclamoModel.usuario_id')
    adhesiones = relationship('AdhesionModel', back_populates='usuario')