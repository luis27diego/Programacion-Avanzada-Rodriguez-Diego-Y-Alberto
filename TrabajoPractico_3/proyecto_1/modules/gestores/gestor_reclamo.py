import pickle
from typing import List, Optional
from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from modules.dominio.usuario import Claustro, Estado, Rol, UsuarioDominio
from modules.dominio.reclamo import ReclamoDominio
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class GestorDeReclamo:
    def __init__(self, reclamo_repositorio: RepositorioAbstracto, clasificador):
        """
        Inicializa el gestor con una instancia del repositorio.
        :param repositorio: Implementación concreta de RepositorioAbstracto (UsuarioRepositorio).
        """
        self.reclamo_repositorio = reclamo_repositorio
        self.mapeo_etiquetas = {
            "soporte informático": 1,
            "maestranza": 2,
            "secretaría técnica": 3
        }
        self.clasificador = clasificador

    def crear_reclamo(self, usuario_id: int, contenido: str, timestamp: datetime, estado: Estado) -> ReclamoDominio:
        if not all ([usuario_id, contenido, timestamp, estado]):
            raise ValueError("Todos los campos son obligatorios para crear un reclamo.")
        
        departamento_id = self.clasificar_reclamo(contenido)
        reclamo = ReclamoDominio(
            id=None,
            usuario_id=usuario_id,
            contenido=contenido,
            timestamp=timestamp,
            estado=estado,
            departamento_id=departamento_id,
            tiempo_resolucion=None
        )
        try:
            return self.reclamo_repositorio.guardar_registro(reclamo)
        except IntegrityError:
            raise ValueError("Error al guardar el reclamo. Problema de integridad de datos.")

    def clasificar_reclamo(self, reclamo: str) -> ReclamoDominio:
        """
        Clasifica el reclamo utilizando el clasificador de texto.
        :param reclamo: Instancia de ReclamoDominio a clasificar.
        :return: Instancia de ReclamoDominio con la etiqueta asignada.
        """
        etiqueta = self.clasificador.clasificar([reclamo])
        etiqueta_departamento = etiqueta[0]
        departamento_id = self.mapeo_etiquetas.get(etiqueta_departamento)
        return departamento_id
    
    def obtener_todos_los_reclamos(self) -> List[ReclamoDominio]:
        """
        Obtiene todos los reclamos almacenados en el repositorio.
        :return: Lista de instancias de ReclamoDominio.
        """
        return self.reclamo_repositorio.obtener_todos_los_registros()

    def obtener_reclamos_departamento(self, departamento_id: int) -> List[ReclamoDominio]:
        """
        Obtiene todos los reclamos asociados a un departamento específico.
        :param departamento_id: ID del departamento.
        :return: Lista de instancias de ReclamoDominio.
        """
        return self.reclamo_repositorio.obtener_registros_por_filtro('departamento_id', departamento_id)
    
    def obtener_reclamos_por_departamento_excluir_usuario(self, departamento_id: int, usuario_id: int) -> List[ReclamoDominio]:
        """
        Obtiene todos los reclamos asociados a un departamento específico, excluyendo los creados por un usuario dado.
        :param departamento_id: ID del departamento.
        :param usuario_id: ID del usuario a excluir.
        :return: Lista de instancias de ReclamoDominio.
        """
        reclamos = self.reclamo_repositorio.obtener_reclamos_sin_usuario_en_departamento(usuario_id, departamento_id)
        return reclamos

if __name__ == "__main__":
    from modules.factoria import crear_repositorio
    usuario_repo, reclamo_repo, departamento_repo = crear_repositorio()
    with open('../../data/claims_clf.pkl', 'rb') as archivo: # para debugear usar esta ruta './data/claims_clf.pkl'
        clf = pickle.load(archivo)

    # Ejemplo de uso
    gestor = GestorDeReclamo(reclamo_repo, clf)
    gestor.crear_reclamo(
        usuario_id=6,
        contenido="Es insoportable trabajar con este sistema, necesito ayuda urgente.",
        timestamp=datetime.now(),
        estado=Estado.PENDIENTE
    )