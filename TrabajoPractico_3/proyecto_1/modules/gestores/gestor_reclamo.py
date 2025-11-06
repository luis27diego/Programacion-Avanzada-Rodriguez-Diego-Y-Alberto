from typing import List, Optional
from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from modules.dominio.reclamo import ReclamoDominio,AdhesionDominio,Estado
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from modules.utilidades.comparador_de_reclamos import ComparadorDeReclamosABC  

class GestorDeReclamo:
    def __init__(self, reclamo_repositorio: RepositorioAbstracto, usuario_repositorio: RepositorioAbstracto, adhesion_repositorio: RepositorioAbstracto):
        """
        Inicializa el gestor con una instancia del repositorio.
        :param repositorio: Implementación concreta de RepositorioAbstracto (UsuarioRepositorio).
        """
        self.__reclamo_repositorio = reclamo_repositorio
        self.__usuario_repositorio = usuario_repositorio
        self.__adhesion_repositorio = adhesion_repositorio
        self.__mapeo_etiquetas = {
            "soporte informático": 2,
            "maestranza": 1,
            "secretaría técnica": 3
        }


    def crear_reclamo(self, usuario_id: int, contenido: str, timestamp: datetime, estado: Estado, departamento_id: int = None) -> ReclamoDominio:
        if not all ([usuario_id, contenido, timestamp, estado]):
            raise ValueError("Todos los campos son obligatorios para crear un reclamo.")
        
        if departamento_id is None:
            departamento_id = self.clasificar_reclamo(contenido)
        reclamo = ReclamoDominio(
            id=None,
            usuario_id=usuario_id,
            contenido=contenido,
            timestamp=timestamp,
            estado=estado,
            departamento_id=departamento_id
        )
        try:
            return self.__reclamo_repositorio.guardar_registro(reclamo)
        except IntegrityError:
            raise ValueError("Error al guardar el reclamo. Problema de integridad de datos.")
    
    def adherir_usuario_a_reclamo(self, id_usuario: int, id_reclamo: int) -> None:
        """
        Crea una adhesión entre un usuario y un reclamo.
        :param id_usuario: ID del usuario.
        :param id_reclamo: ID del reclamo.
        :raises ValueError: Si el usuario o reclamo no existen, o si ya está adherido.
        """
        usuario = self.__usuario_repositorio.obtener_registro_por_filtro('id', id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe.")
        
        # Verificar si el reclamo existe (puedes extender el repositorio para incluir esta validación)
        # Aquí asumimos que el repositorio lanza una excepción si la adhesión falla
        try:
            self.__adhesion_repositorio.guardar_registro(AdhesionDominio(usuario_id=id_usuario, reclamo_id=id_reclamo))
        except IntegrityError as e:
            raise ValueError(f"Error al adherir al reclamo: {str(e)}")

    def clasificar_reclamo(self, reclamo: str, clasificador) -> int:
        """
        Clasifica el reclamo utilizando el clasificador de texto.
        :param reclamo: contenido de ReclamoDominio a clasificar.
        :return: ID del departamento asignado.
        """
        etiqueta = clasificador.classify([reclamo])
        etiqueta_departamento = etiqueta[0]
        departamento_id = self.__mapeo_etiquetas.get(etiqueta_departamento)
        return departamento_id

    def encontrar_reclamos_similares(self, contenido, reclamos, comparador: ComparadorDeReclamosABC):
        if not isinstance(comparador, ComparadorDeReclamosABC):
            raise TypeError("comparador debe implementar ComparadorDeReclamosABC")
        return comparador.encontrar_reclamos_similares(contenido, reclamos)

    def obtener_todos_los_reclamos(self) -> List[ReclamoDominio]:
        """
        Obtiene todos los reclamos almacenados en el repositorio.
        :return: Lista de instancias de ReclamoDominio.
        """
        return self.__reclamo_repositorio.obtener_todos_los_registros()
    
    def obtener_reclamos_por_estado(self, estado: Estado) -> List[ReclamoDominio]:
        """
        Obtiene todos los reclamos que coinciden con un estado específico.
        :param estado: Estado por el cual filtrar los reclamos.
        :return: Lista de instancias de ReclamoDominio.
        """
        return self.__reclamo_repositorio.obtener_registros_por_filtro('estado', estado)
    
    def obtener_reclamo_por_id(self, reclamo_id: int) -> List[ReclamoDominio]:
        """
        Obtiene un reclamo por su ID.
        :param reclamo_id: ID del reclamo.
        :return: Instancia de ReclamoDominio o None si no se encuentra.
        """
        return self.__reclamo_repositorio.obtener_registro_por_filtro('id', reclamo_id)

    def obtener_reclamos_departamento(self, departamento_id: int) -> List[ReclamoDominio]:
        """
        Obtiene todos los reclamos asociados a un departamento específico.
        :param departamento_id: ID del departamento.
        :return: Lista de instancias de ReclamoDominio.
        """
        return self.__reclamo_repositorio.obtener_registros_por_filtro('departamento_id', departamento_id)
    
    def obtener_reclamos_por_departamento_excluir_usuario(self, departamento_id: int, usuario_id: int) -> List[ReclamoDominio]:
        """
        Obtiene todos los reclamos asociados a un departamento específico, excluyendo los creados por un usuario dado.
        :param departamento_id: ID del departamento.
        :param usuario_id: ID del usuario a excluir.
        :return: Lista de instancias de ReclamoDominio.
        """
        reclamos = self.__reclamo_repositorio.obtener_registros_por_filtro('departamento_id', departamento_id)
        reclamos = [r for r in reclamos if r.usuario_id != usuario_id]
        return reclamos
    
    def modificar_estado_reclamo(self, reclamo_id: int, nuevo_estado: Estado) -> Optional[ReclamoDominio]:
        """
        Modifica el estado de un reclamo existente.
        :param reclamo_id: ID del reclamo a modificar.
        :param nuevo_estado: Nuevo estado a asignar.
        :return: Instancia de ReclamoDominio modificada o None si no se encuentra.
        """
        reclamo = self.__reclamo_repositorio.obtener_registro_por_filtro('id', reclamo_id)
        if reclamo:
            reclamo.estado = nuevo_estado
            reclamo.timestamp_modificacion = datetime.now()
            return self.__reclamo_repositorio.modificar_registro(reclamo)
        return None
    
    def modificar_departamento_reclamo(self, id_reclamo, nuevo_departamento_id):
        """
        Modifica el departamento asignado a un reclamo existente.
        :param id_reclamo: ID del reclamo a modificar.
        :param nuevo_departamento_id: Nuevo ID de departamento a asignar.
        :return: Instancia de ReclamoDominio modificada o None si no se encuentra.
        """
        reclamo = self.__reclamo_repositorio.obtener_registro_por_filtro('id', id_reclamo)
        if reclamo:
            reclamo.departamento_id = nuevo_departamento_id
            return self.__reclamo_repositorio.modificar_registro(reclamo)
        return None

    def obtener_reclamos_creados_por_usuario(self, id_usuario: int) -> List[ReclamoDominio]:
        """
        Obtiene los reclamos creados por un usuario.
        :param id_usuario: ID del usuario.
        :return: Lista de ReclamoDominio.
        """
        usuario = self.__usuario_repositorio.obtener_registro_por_filtro('id', id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe.")
        return self.__reclamo_repositorio.obtener_registros_por_filtro('usuario_id', id_usuario)

    def obtener_reclamos_adheridos_por_usuario(self, id_usuario: int) -> List[ReclamoDominio]:
        """
        Obtiene los reclamos a los que un usuario se adhirió.
        :param id_usuario: ID del usuario.
        :return: Lista de ReclamoDominio.
        """
        usuario = self.__usuario_repositorio.obtener_registro_por_filtro('id', id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe.")
        return self.__adhesion_repositorio.obtener_registros_por_filtro('usuario_id', id_usuario)

if __name__ == "__main__":
    import pickle
    from modules.factoria import crear_repositorio
    usuario_repo, reclamo_repo, departamento_repo = crear_repositorio()
    with open('./data/claims_clf.pkl', 'rb') as archivo: # para debugear usar esta ruta './data/claims_clf.pkl'
        clf = pickle.load(archivo)

    # Ejemplo de uso
    gestor = GestorDeReclamo(reclamo_repo, clf)
    gestor.modificar_estado_reclamo(2, Estado.EN_PROCESO)
    """     reclamo_creado =gestor.crear_reclamo(
        usuario_id=6,
        contenido="Es insoportable trabajar con este sistema, necesito ayuda urgente.",
        timestamp=datetime.now(),
        estado=Estado.PENDIENTE
    ) """

    

