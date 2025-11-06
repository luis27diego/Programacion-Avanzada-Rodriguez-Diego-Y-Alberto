from enum import Enum
from modules.dominio.reclamo import ReclamoDominio
from abc import ABC

class UsuarioDominio(ABC):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, 
                 password: str, id: int = None):
        self.id = id
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__usuario = usuario
        self.__password = password

    @property
    def password(self):
        return self.__password

    @property
    def nombre(self):
        return self.__nombre
    @property
    def apellido(self):
        return self.__apellido
    @property
    def email(self):
        return self.__email
    @property
    def usuario(self):
        return self.__usuario


class UsuarioFinal(UsuarioDominio):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, 
                 claustro: str, password: str, id: int = None):
        super().__init__(nombre, apellido, email, usuario, password, id)
        self.__claustro = claustro
        self.__reclamos_creados = []
        self.__reclamos_adheridos = []
    @property
    def claustro(self):
        return self.__claustro
    def agregar_reclamo_creado(self, reclamo: int):
        if any(r == reclamo for r in self.__reclamos_creados):
            raise ValueError("Reclamo ya agregado")
        self.__reclamos_creados.append(reclamo)

    def agregar_reclamo_adherido(self, reclamo: int):
        if any(r == reclamo for r in self.__reclamos_adheridos):
            raise ValueError("Ya adherido a este reclamo")
        self.__reclamos_adheridos.append(reclamo)

    def obtener_reclamos_creados(self):
        return self.__reclamos_creados[:]

    def obtener_reclamos_adheridos(self):
        return self.__reclamos_adheridos[:]

class ResponsableDepartamento(UsuarioDominio):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, 
                 password: str, rol: str, id: int = None, departamento_id: int = None):

        super().__init__(nombre, apellido, email, usuario, password, id)
        self.__rol = rol
        self.__departamento_id = departamento_id

    @property
    def rol(self):
        return self.__rol
    @property
    def departamento_id(self):
        return self.__departamento_id

if __name__ == "__main__":
    usuario = UsuarioFinal(
        nombre="Juan",
        apellido="Perez",
        email="juan.perez@example.com",
        usuario="juanp",
        claustro='estudiante',
        password="password123"
    )
    print(f"Usuario creado: {usuario.nombre} {usuario.apellido}, Claustro: {usuario.claustro}")

    responsable = ResponsableDepartamento(
        nombre="Ana",
        apellido="Gomez",
        email="ana.gomez@example.com",
        usuario="anag",
        password="password456",
        rol='jefe_departamento',
        departamento_id=1
    )
    print(f"Responsable creado: {responsable.nombre} {responsable.apellido}, Rol: {responsable.rol}, Departamento ID: {responsable.departamento_id}")

    responsable_secretario = ResponsableDepartamento(
        nombre="Luis",
        apellido="Martinez",
        email="luis.martinez@example.com",
        usuario="luism",
        password="password789",
        rol='secretario_tecnico',
        departamento_id=1
    )
    print(f"Responsable creado: {responsable_secretario.nombre} {responsable_secretario.apellido}, Rol: {responsable_secretario.rol}, Departamento ID: {responsable_secretario.departamento_id}")