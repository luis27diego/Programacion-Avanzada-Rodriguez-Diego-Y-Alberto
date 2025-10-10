
from modules.dominio.usuario import UsuarioDominio
class DepartamentoDominio:
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre
        self._users_asociados = []  # Lista de UsuarioDominio (jefes/secretario)

    def agregar_user_asociado(self, user: UsuarioDominio):
        if user.department_id != self.id:
            raise ValueError("User no pertenece a este departamento")
        self._users_asociados.append(user)

    def get_users_asociados(self) -> list[UsuarioDominio]:
        return self._users_asociados[:]