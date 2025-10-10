from modules.dominio.usuario import UsuarioDominio
from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required, current_user
from flask import abort
from functools import wraps

class FlaskLoginUser(UserMixin):
    def __init__(self,  usuario_dominio: UsuarioDominio):
        self.id = usuario_dominio.id
        self.nombre = usuario_dominio.nombre
        self.email = usuario_dominio.email
        self.password = usuario_dominio.password

class GestorDeLogin:
    def __init__(self, gestor_usuarios, login_manager, admin_list):
        self.__gestor_usuarios = gestor_usuarios
        login_manager.user_loader(self.__cargar_usuario_actual)
        self.__admin_list = admin_list

    def __cargar_usuario_actual(self, user_id):
        usuario = self.__gestor_usuarios.obtener_usuario_por_id(user_id)
        if usuario:
            return FlaskLoginUser(usuario)
        return None

    @property
    def nombre_usuario_actual(self):
        return current_user.nombre

    @property
    def id_usuario_actual(self):
        return current_user.id
    
    @property
    def usuario_autenticado(self):
        return current_user.is_authenticated
    
    def login_usuario(self, usuario_dominio: UsuarioDominio):
        user = FlaskLoginUser(usuario_dominio)
        login_user(user)
        print(f"Usuario {current_user.nombre} ha iniciado sesión")

    def logout_usuario(self):
        logout_user()
        print("Usuario ha cerrado sesión")
        print(f"Usuario actual {current_user}")

    def se_requiere_login(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("¿Está autenticado?", current_user.is_authenticated)
            return login_required(func)(*args, **kwargs)
        return wrapper