
from modules.dominio.usuario import ResponsableDepartamento
class DepartamentoDominio:
    def __init__(self, id: int, nombre: str):
        self.__id = id
        self.__nombre = nombre
        self._users_asociados = []  # Lista de UsuarioDominio (jefes/secretario)
    @property
    def id(self) -> int:
        return self.__id
    @property
    def nombre(self) -> str:
        return self.__nombre

    def agregar_user_asociado(self, user: ResponsableDepartamento):
        if user.departamento_id != self.id:
            raise ValueError("User no pertenece a este departamento")
        self._users_asociados.append(user)

    def get_users_asociados(self) -> list[ResponsableDepartamento]:
        return self._users_asociados[:]