from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from sqlalchemy.orm import Session
from modules.dominio.reclamo import AdhesionDominio, ReclamoDominio
from modules.modelos.adhesionModel import AdhesionModel
from modules.modelos.reclamoModel import ReclamoModel


class AdhesionRepositorio(RepositorioAbstracto):
    def __init__(self, session: Session):
        self.__session = session

    def guardar_registro(self, adhesion: AdhesionDominio) -> None:
        adhesion_modelo = self.__dominio_to_modelo(adhesion)
        self.__session.add(adhesion_modelo)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        adhesiones_modelos = self.__session.query(AdhesionModel).all()
        return [self.__modelo_to_dominio(u) for u in adhesiones_modelos]

    def modificar_registro(self, registro_modificado: AdhesionDominio):
        register = self.__session.query(AdhesionModel).filter_by(id=registro_modificado.id).first()
        register.usuario_id = registro_modificado.usuario_id
        register.reclamo_id = registro_modificado.reclamo_id
        self.__session.commit()
        self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        adhesion_modelo = self.__session.query(AdhesionModel).filter_by(**{filtro: valor}).first()
        if not adhesion_modelo:
            return None
        return self.__modelo_to_dominio(adhesion_modelo)

    def obtener_registros_por_filtro(self, filtros, valor):
        adhesiones_modelos = self.__session.query(ReclamoModel).join(AdhesionModel).filter_by(**{filtros: valor}).all()
        return [self.__modelo_reclamo_to_dominio(u) for u in adhesiones_modelos]

    def eliminar_registro(self, id):
        register = self.__session.query(AdhesionModel).get(id)
        self.__session.delete(register)
        self.__session.commit()

    def __dominio_to_modelo(self, dominio: AdhesionDominio) -> AdhesionModel:
        return AdhesionModel(id=dominio.id, usuario_id=dominio.usuario_id, reclamo_id=dominio.reclamo_id)
    
    def __modelo_reclamo_to_dominio(self, modelo: ReclamoModel) -> ReclamoDominio:
        reclamo = ReclamoDominio(
        id=modelo.id,
        usuario_id=modelo.usuario_id,
        contenido=modelo.contenido,
        timestamp=modelo.timestamp,
        estado=modelo.estado,
        departamento_id=modelo.departamento_id,
        timestamp_modificacion=modelo.timestamp_modificacion,
        )

        adherentes = self.__session.query(AdhesionModel).filter(AdhesionModel.reclamo_id == modelo.id).all()
        for adherente in adherentes:
            reclamo.agregar_adherente(adherente.usuario_id)
        return reclamo

    def __modelo_to_dominio(self, modelo: AdhesionModel) -> AdhesionDominio:
        return AdhesionDominio(id=modelo.id, usuario_id=modelo.usuario_id, reclamo_id=modelo.reclamo_id)