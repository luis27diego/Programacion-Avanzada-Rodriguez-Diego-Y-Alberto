from modules.dominio.usuario import UsuarioDominio,ResponsableDepartamento
from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required, current_user
from flask import abort
from functools import wraps
from flask import redirect, url_for, flash, render_template

class FlaskLoginUser(UserMixin):
    def __init__(self,  usuario_dominio: UsuarioDominio):
        self.id = usuario_dominio.id
        self.nombre = usuario_dominio.nombre
        self.email = usuario_dominio.email
        self.password = usuario_dominio.password
        self.admin = isinstance(usuario_dominio, ResponsableDepartamento) 
class GestorDeLogin:
    def __init__(self, gestor_usuarios, login_manager):
        self.__gestor_usuarios = gestor_usuarios
        login_manager.user_loader(self.__cargar_usuario_actual)

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
    
    @property
    def es_admin(self):
        return current_user.is_authenticated and current_user.admin
    
    def login_usuario(self, usuario_dominio: UsuarioDominio):
        user = FlaskLoginUser(usuario_dominio)
        login_user(user)
        print(f"Usuario {current_user.nombre} ha iniciado sesión")

    def logout_usuario(self):
        logout_user()
        print("Usuario ha cerrado sesión")
        print(f"Usuario actual {current_user}")

    
    def admin_only(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Por favor, inicia sesión como administrador para acceder a esta página.")
                return redirect(url_for('login'))
            elif not current_user.admin:
                return render_template('error.html', error="Acceso denegado: área restringida para administradores.", es_admin=False)
            return f(*args, **kwargs)
        return decorated_function

    def solo_usuarios_no_admin(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Por favor, inicia sesión para acceder a esta página.")
                return redirect(url_for('login'))
            elif current_user.admin:
                return render_template('error.html', error="Acceso denegado: área restringida para administradores. Solo usuarios finales.", es_admin=True)
                #abort(403)
        
            return f(*args, **kwargs)
        return decorated_function