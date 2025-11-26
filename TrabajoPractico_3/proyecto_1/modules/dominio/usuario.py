from enum import Enum
from modules.dominio.reclamo import ReclamoDominio
from abc import ABC

class UsuarioDominio(ABC):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, 
                 password: str, id: int = None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.usuario = usuario
        self.password = password

    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self, valor: str):
        if not valor or len(valor) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres")
        self.__password = valor  

    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = valor.strip().title()

    @property
    def apellido(self):
        return self.__apellido
    @apellido.setter
    def apellido(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El apellido no puede estar vacío")
        self.__apellido = valor.strip().title()

    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise ValueError("Email inválido")
        self.__email = valor.strip().lower()

    @property
    def usuario(self):
        return self.__usuario
    @usuario.setter
    def usuario(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise ValueError("El usuario debe tener al menos 3 caracteres")
        self.__usuario = valor.strip().lower()


class UsuarioFinal(UsuarioDominio):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, 
                 claustro: str, password: str, id: int = None):
        super().__init__(nombre, apellido, email, usuario, password, id)
        self.claustro = claustro
        self.__reclamos_creados = []
        self.__reclamos_adheridos = []
    @property
    def claustro(self):
        return self.__claustro
    @claustro.setter
    def claustro(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El claustro no puede estar vacío")
        if valor.strip().lower() not in ['estudiante', 'docente', 'pays']:
            raise ValueError("El claustro debe ser 'estudiante', 'docente' o 'no docente'")
        self.__claustro = valor.strip().lower()

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