from abc import ABC, abstractmethod

class RepositorioAbstracto(ABC):
    @abstractmethod
    def guardar_registro(self, registro):
        raise NotImplementedError

    @abstractmethod
    def obtener_todos_los_registros(self):
        raise NotImplementedError
    
    @abstractmethod
    def modificar_registro(self, registro_modificado):
        raise NotImplementedError
    
    @abstractmethod
    def obtener_registro_por_filtro(self, filtro, valor):
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_registro(self, id):
        raise NotImplementedError
    
    @abstractmethod
    def crear_relacion(self, id_objeto_1: int, id_objeto_2: int, tipo_relacion: str) -> None:
        pass
