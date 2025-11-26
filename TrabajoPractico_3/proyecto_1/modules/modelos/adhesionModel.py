
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from . import Base


class AdhesionModel(Base):
    __tablename__ = 'adhesiones'

    id = Column(Integer, primary_key=True, autoincrement=True)  
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False, index=True)
    reclamo_id = Column(Integer, ForeignKey('reclamos.id'), nullable=False, index=True)

    usuario = relationship('UsuarioModel', back_populates='adhesiones')
    reclamo = relationship('ReclamoModel', backref='adhesiones')