from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from sqlalchemy.orm import Session
from modules.dominio.usuario import UsuarioDominio, UsuarioFinal,ResponsableDepartamento
#from modules.dominio.reclamo import ReclamoDominio
from modules.modelos.reclamoModel import ReclamoModel
from modules.modelos.usuarioModel import UsuarioModel
from modules.modelos.adhesionModel import AdhesionModel
#from modules.modelos.departamentoModel import DepartamentoModel

class UsuarioRepositorio(RepositorioAbstracto):
    def __init__(self, session: Session):
        self.__session = session

    def guardar_registro(self, usuario: UsuarioDominio) -> None:            
        usuario_modelo = self.__dominio_to_modelo(usuario)
        self.__session.add(usuario_modelo)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        usuarios_modelos = self.__session.query(UsuarioModel).all()
        return [self.__modelo_to_dominio(u) for u in usuarios_modelos]

    def modificar_registro(self, registro_modificado: UsuarioDominio):
        register = self.__session.query(UsuarioModel).filter_by(id=registro_modificado.id).first()
        register.nombre = registro_modificado.nombre
        register.apellido = registro_modificado.apellido
        register.email = registro_modificado.email
        register.usuario = registro_modificado.usuario
        register.claustro = registro_modificado.claustro
        register.password = registro_modificado.password
        register.rol = registro_modificado.rol
        register.departamento_id = registro_modificado.departamento_id
        self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        usuario_modelo = self.__session.query(UsuarioModel).filter_by(**{filtro: valor}).first()
        if not usuario_modelo:
            return None
        usuario = self.__modelo_to_dominio(usuario_modelo)
        return usuario

    def obtener_registros_por_filtro(self, filtros, valor):
        usuarios_modelos = self.__session.query(UsuarioModel).filter_by(**{filtros: valor}).all()
        return [self.__modelo_to_dominio(u) for u in usuarios_modelos]

    def eliminar_registro(self, id):
        register = self.__session.query(UsuarioModel).get(id)
        self.__session.delete(register)
        self.__session.commit()

    def __modelo_to_dominio(self, modelo: UsuarioModel) -> UsuarioDominio:
        if modelo.rol is None:
            usuario_final = UsuarioFinal(
                id=modelo.id,
                nombre=modelo.nombre,
                apellido=modelo.apellido,
                email=modelo.email,
                usuario=modelo.usuario,
                claustro=modelo.claustro,
                password=modelo.password
            )
            # Cargar reclamos creados y adheridos incrementalmente
            reclamos_modelos = self.__session.query(ReclamoModel).filter(ReclamoModel.usuario_id == modelo.id).all()
            for reclamo_modelo in reclamos_modelos:
                usuario_final.agregar_reclamo_creado(reclamo_modelo.id)
            reclamos_adheridos_modelos = self.__session.query(ReclamoModel).join(AdhesionModel).filter(AdhesionModel.usuario_id == modelo.id).all()
            for reclamo_modelo in reclamos_adheridos_modelos:
                usuario_final.agregar_reclamo_adherido(reclamo_modelo.id)
            return usuario_final
        else:
            responsable = ResponsableDepartamento(
                id=modelo.id,
                nombre=modelo.nombre,
                apellido=modelo.apellido,
                email=modelo.email,
                usuario=modelo.usuario,
                password=modelo.password,
                rol=modelo.rol,
                departamento_id=modelo.departamento_id
            )
            return responsable

    def __dominio_to_modelo(self, dominio: UsuarioDominio) -> UsuarioModel:
        return UsuarioModel(
            id=dominio.id,
            nombre=dominio.nombre,
            apellido=dominio.apellido,
            email=dominio.email,
            usuario=dominio.usuario,
            claustro=dominio.claustro if hasattr(dominio, 'claustro') else None,
            password=dominio.password,
            rol=dominio.rol if hasattr(dominio, 'rol') else None,
            departamento_id=dominio.departamento_id if hasattr(dominio, 'departamento_id') else None
        )