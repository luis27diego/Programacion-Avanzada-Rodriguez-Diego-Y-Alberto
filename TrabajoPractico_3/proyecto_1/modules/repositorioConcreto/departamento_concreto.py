from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from sqlalchemy.orm import Session
from modules.dominio.departamento import DepartamentoDominio
from modules.modelos.departamentoModel import DepartamentoModel


class DepartamentoRepositorio(RepositorioAbstracto):
    def __init__(self, session: Session):
        self.__session = session

    def guardar_registro(self, departamento: DepartamentoDominio) -> None:
        departamento_modelo = self.__dominio_to_modelo(departamento)
        self.__session.add(departamento_modelo)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        departamentos_modelos = self.__session.query(DepartamentoModel).all()
        return [self.__modelo_to_dominio(u) for u in departamentos_modelos]

    def modificar_registro(self, registro_modificado: DepartamentoDominio):
        register = self.__session.query(DepartamentoModel).filter_by(id=registro_modificado.id).first()
        register.nombre = registro_modificado.nombre
        self.__session.commit()
        self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        departamento_modelo = self.__session.query(DepartamentoModel).filter_by(**{filtro: valor}).first()
        if not departamento_modelo:
            return None
        departamento = self.__modelo_to_dominio(departamento_modelo)
        return departamento
    
    def obtener_registros_por_filtro(self, filtros, valor):
        departamentos_modelos = self.__session.query(DepartamentoModel).filter_by(**{filtros: valor}).all()
        return [self.__modelo_to_dominio(u) for u in departamentos_modelos]
            
    def eliminar_registro(self, id):
        register = self.__session.query(DepartamentoModel).get(id)
        self.__session.delete(register)
        self.__session.commit()

    def __dominio_to_modelo(self, dominio: DepartamentoDominio) -> DepartamentoModel:
        return DepartamentoModel(id=dominio.id, nombre=dominio.nombre)
    
    def __modelo_to_dominio(self, modelo: DepartamentoModel) -> DepartamentoDominio:
        return DepartamentoDominio(id=modelo.id, nombre=modelo.nombre)