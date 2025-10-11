from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from sqlalchemy.orm import Session
from sqlalchemy import not_
from modules.dominio.usuario import UsuarioDominio
from modules.dominio.reclamo import ReclamoDominio
from modules.modelos.reclamoModel import ReclamoModel
from modules.modelos.usuarioModel import UsuarioModel
from modules.modelos.adhesionModel import AdhesionModel
from modules.modelos.departamentoModel import DepartamentoModel


class ReclamoRepositorio(RepositorioAbstracto):
    def __init__(self, session: Session):
        self.__session = session

    def guardar_registro(self, reclamo: ReclamoDominio) -> None:
        reclamo_modelo = self.__dominio_to_modelo(reclamo)
        self.__session.add(reclamo_modelo)
        self.__session.commit()
        self.__session.refresh(reclamo_modelo)  # Asegura que el modelo tenga el ID asignado
        return self.__modelo_to_dominio(reclamo_modelo)

    def obtener_todos_los_registros(self):
        reclamos_modelos = self.__session.query(ReclamoModel).all()
        return [self.__modelo_to_dominio(u) for u in reclamos_modelos]

    def modificar_registro(self, registro_modificado: ReclamoDominio):
        register = self.__session.query(ReclamoModel).filter_by(id=registro_modificado.id).first()
        register.contenido = registro_modificado.contenido
        register.timestamp = registro_modificado.timestamp
        register.timestamp_modificacion = registro_modificado.timestamp_modificacion
        register.estado = registro_modificado.estado.name if hasattr(registro_modificado.estado, 'name') else registro_modificado.estado
        register.departamento_id = registro_modificado.departamento_id
        self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        reclamo_modelo = self.__session.query(ReclamoModel).filter_by(**{filtro: valor}).first()
        if not reclamo_modelo:
            return None
        reclamo = self.__modelo_to_dominio(reclamo_modelo)
        return reclamo

    def obtener_registros_por_filtro(self, filtros, valor):
        reclamos_modelos = self.__session.query(ReclamoModel).filter_by(**{filtros: valor}).all()
        return [self.__modelo_to_dominio(u) for u in reclamos_modelos]

    def obtener_reclamos_sin_usuario_en_departamento(self, usuario_id: int, departamento_id: int):
        subquery = self.__session.query(AdhesionModel).filter(
            AdhesionModel.usuario_id == usuario_id,  # cambiar a id_usuario si ya lo corregiste
            AdhesionModel.reclamo_id == ReclamoModel.id
        ).exists()

        reclamos_filtrados = self.__session.query(ReclamoModel).filter(
            ReclamoModel.usuario_id != usuario_id,
            ReclamoModel.departamento_id == departamento_id,
            not_(subquery)
        )

        return [self.__modelo_to_dominio(u) for u in reclamos_filtrados.all()]

    def crear_relacion(self, id_usuario: int, id_reclamo: int, tipo_relacion: str) -> None:
        if tipo_relacion == 'adhesion':
            adhesion = AdhesionModel(usuario_id=id_usuario, reclamo_id=id_reclamo)
            self.__session.add(adhesion)
            self.__session.commit()

    def eliminar_registro(self, id):
        register = self.__session.query(ReclamoModel).get(id)
        self.__session.delete(register)
        self.__session.commit()


    def __modelo_to_dominio(self, modelo: ReclamoModel) -> ReclamoDominio:
        reclamo = ReclamoDominio(
            id=modelo.id,
            usuario_id=modelo.usuario_id,
            contenido=modelo.contenido,
            timestamp=modelo.timestamp,
            estado=modelo.estado,
            departamento_id=modelo.departamento_id,
            timestamp_modificacion=modelo.timestamp_modificacion,
        )
        # Cargar creador y adherentes si están en DB
        creador = self.__session.query(UsuarioModel).filter(UsuarioModel.id == modelo.usuario_id).first()
        if creador:
            creador_domain = self.__modelo_usuario_to_dominio(creador)
            reclamo.asignar_creador(creador_domain)


        adherentes = self.__session.query(UsuarioModel).join(AdhesionModel).filter(AdhesionModel.reclamo_id == modelo.id).all()
        for adherente in adherentes:
            adherente_domain = self.__modelo_usuario_to_dominio(adherente)
            reclamo.agregar_adherente(adherente_domain)
        return reclamo

    def __dominio_to_modelo(self, dominio: ReclamoDominio) -> ReclamoModel:
        return ReclamoModel(
            id=dominio.id,
            usuario_id=dominio.usuario_id,
            contenido=dominio.contenido,
            timestamp=dominio.timestamp,
            estado=dominio.estado.name if hasattr(dominio.estado, 'name') else dominio.estado,
            departamento_id=dominio.departamento_id,
            timestamp_modificacion=dominio.timestamp_modificacion,
        )
    
    def __modelo_usuario_to_dominio(self, modelo: UsuarioModel) -> UsuarioDominio:
        usuario =UsuarioDominio(
        id=modelo.id,
        nombre=modelo.nombre,
        apellido=modelo.apellido,
        email=modelo.email,
        usuario=modelo.usuario,
        claustro=modelo.claustro,
        password=modelo.password,
        rol=modelo.rol,
        departamento_id=modelo.departamento_id
    )
        # Cargar reclamos creados y adheridos incrementalmente
        reclamos_modelos = self.__session.query(ReclamoModel).filter(ReclamoModel.usuario_id == modelo.id).all()
        for reclamo_modelo in reclamos_modelos:
            reclamo = ReclamoDominio(
                id=reclamo_modelo.id,
                usuario_id=reclamo_modelo.usuario_id,
                contenido=reclamo_modelo.contenido,
                timestamp=reclamo_modelo.timestamp,
                estado=reclamo_modelo.estado,
                departamento_id=reclamo_modelo.departamento_id,
                timestamp_modificacion=reclamo_modelo.timestamp_modificacion,
            )
            usuario.agregar_reclamo_creado(reclamo)
        reclamos_adheridos_modelos = self.__session.query(ReclamoModel).join(AdhesionModel).filter(AdhesionModel.usuario_id == modelo.id).all()
        for reclamo_modelo in reclamos_adheridos_modelos:
            reclamo = ReclamoDominio(
                id=reclamo_modelo.id,
                usuario_id=reclamo_modelo.usuario_id,
                contenido=reclamo_modelo.contenido,
                timestamp=reclamo_modelo.timestamp,
                estado=reclamo_modelo.estado,
                departamento_id=reclamo_modelo.departamento_id,
                timestamp_modificacion=reclamo_modelo.timestamp_modificacion,
            )
            usuario.agregar_reclamo_adherido(reclamo)
        return usuario