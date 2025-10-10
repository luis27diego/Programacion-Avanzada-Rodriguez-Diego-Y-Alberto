from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from . import Base

class DepartamentoModel(Base):
    __tablename__ = 'departamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    usuarios = relationship('UsuarioModel', back_populates='departamento')
    reclamos = relationship('ReclamoModel', back_populates='departamento')