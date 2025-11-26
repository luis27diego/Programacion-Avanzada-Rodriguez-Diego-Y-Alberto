from typing import List, Optional
from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from modules.dominio.usuario import UsuarioDominio, UsuarioFinal, ResponsableDepartamento
from sqlalchemy.exc import IntegrityError

class GestorDeUsuarios:
    def __init__(self, usuario_repositorio: RepositorioAbstracto):
        """
        Inicializa el gestor con una instancia del repositorio.
        :param repositorio: Implementación concreta de RepositorioAbstracto (UsuarioRepositorio).
        """
        self.__usuario_repositorio = usuario_repositorio

    def crear_usuario(self, nombre: str, apellido: str, email: str, usuario: str, password: str, claustro: str) -> UsuarioDominio:
        """
        Crea un nuevo usuario en el repositorio.
        :param usuario: Objeto UsuarioDominio a guardar.
        :return: El usuario guardado.
        :raises ValueError: Si faltan datos obligatorios o el email/usuario ya existe.
        """
        # Validaciones básicas
        if not all([nombre, apellido, email, usuario, password]):
            raise ValueError("Faltan datos obligatorios para crear el usuario.")
        
        # Verificar unicidad de email y usuario
        if self.obtener_usuario_por_email(email):
            raise ValueError("El email ya está registrado.")
        if self.obtener_usuario_por_usuario(usuario):
            raise ValueError("El nombre de usuario ya está registrado.")
        
        try:
            usuario = UsuarioFinal(
                id=None,
                nombre=nombre,
                apellido=apellido,
                email=email,
                usuario=usuario,
                password=password,
                claustro=claustro,
            )
            self.__usuario_repositorio.guardar_registro(usuario)
            return self.obtener_usuario_por_email(email)  # Retorna el usuario con ID
        except IntegrityError as e:
            raise ValueError(f"Error al crear el usuario: {str(e)}")

    def obtener_todos_los_usuarios(self) -> List[UsuarioDominio]:
        """
        Obtiene todos los usuarios del repositorio.
        :return: Lista de objetos UsuarioDominio.
        """
        return self.__usuario_repositorio.obtener_todos_los_registros()

    def modificar_usuario(self, id: int, nombre: str, apellido: str, email: str, usuario: str, password: str, claustro: str = None, rol: str = None, departamento_id: int = None) -> UsuarioDominio:
        """
        Modifica un usuario existente.
        :param usuario_modificado: Objeto UsuarioDominio con los cambios.
        :return: El usuario modificado.
        :raises ValueError: Si el usuario no existe o los datos son inválidos.
        """
        if id is None:
            raise ValueError("El usuario debe tener un ID para modificarlo.")
        
        # Verificar que el usuario existe
        usuario_actual = self.obtener_usuario_por_id(id)
        if not usuario_actual:
            raise ValueError("El usuario no existe.")
        
        # Validar unicidad de email y usuario (si cambiaron)
        if email != usuario_actual.email:
            if self.obtener_usuario_por_email(email):
                raise ValueError("El email ya está registrado.")
        if usuario != usuario_actual.usuario:
            if self.obtener_usuario_por_usuario(usuario):
                raise ValueError("El nombre de usuario ya está registrado.")
            
        if claustro is None:
            try:
                usuario_modificado = UsuarioFinal(
                    id=id,
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    usuario=usuario,
                    password=password,
                    claustro=claustro,
                )
                self.__usuario_repositorio.modificar_registro(usuario_modificado)
                return self.obtener_usuario_por_id(usuario_modificado.id)
            except IntegrityError as e:
                raise ValueError(f"Error al modificar el usuario: {str(e)}")
        else:
            try:
                usuario_modificado = ResponsableDepartamento(
                    id=id,
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    usuario=usuario,
                    password=password,
                    rol=rol,
                    departamento_id=departamento_id
                )
                self.__usuario_repositorio.modificar_registro(usuario_modificado)
                return self.obtener_usuario_por_id(usuario_modificado.id)
            except IntegrityError as e:
                raise ValueError(f"Error al modificar el usuario: {str(e)}")

    def obtener_usuario_por_email(self, email: str) -> UsuarioDominio:
        if not email:
            raise ValueError("El email no puede estar vacío.")

        return self.__usuario_repositorio.obtener_registro_por_filtro('email', email)

    def obtener_usuario_por_id(self, id: int) -> UsuarioDominio:
        if id is None:
            raise ValueError("El ID no puede ser None.")

        return self.__usuario_repositorio.obtener_registro_por_filtro('id', id)

    def obtener_usuario_por_usuario(self, usuario: str) -> UsuarioDominio:
        if not usuario:
            raise ValueError("El nombre de usuario no puede estar vacío.")

        return self.__usuario_repositorio.obtener_registro_por_filtro('usuario', usuario)

    def eliminar_usuario(self, id: int) -> bool:
        """
        Elimina un usuario por ID.
        :param id: ID del usuario a eliminar.
        :return: True si se eliminó exitosamente.
        :raises ValueError: Si el usuario no existe.
        """
        if not self.obtener_usuario_por_id(id):
            raise ValueError("El usuario no existe.")
        try:
            self.__usuario_repositorio.eliminar_registro(id)
            return True
        except IntegrityError as e:
            raise ValueError(f"Error al eliminar el usuario: {str(e)}")

    def autenticar_usuario(self, email: str, password: str) -> Optional[UsuarioDominio]:
        """
        Autentica un usuario por email y contraseña.
        :param email: Email del usuario.
        :param password: Contraseña (sin hashear por simplicidad).
        :return: Objeto UsuarioDominio o ValueError si las credenciales son inválidas.
        """
        
        usuario_dominio = self.obtener_usuario_por_email(email)
        if usuario_dominio is None:
            raise ValueError("El email no está registrado. Por favor, regístrese.")

        if usuario_dominio and usuario_dominio.password == password: 
            return usuario_dominio  
        raise ValueError("Credenciales inválidas. Email y/o contraseña incorrectos.")

    
if __name__ == "__main__":
    import pickle
    from modules.factoria import crear_repositorio
    usuario_repo, reclamo_repo, departamento_repo = crear_repositorio()
    with open('../../data/claims_clf.pkl', 'rb') as archivo: # para debugear usar esta ruta './data/claims_clf.pkl'
        clf = pickle.load(archivo)

    gestor = GestorDeUsuarios(usuario_repo, reclamo_repo, clf)

    usuario_creado = gestor.crear_usuario(
        nombre="Alberto",
        apellido="Aguilar",
        email="Alberto@example.com",
        usuario="AlbertoAguilar",
        claustro='ESTUDIANTE',
        password="password123545",
        )
    print(f"Usuario creado con ID: {usuario_creado.id}")

    gestor.modificar_usuario(
        id=usuario_creado.id,
        nombre="Juan",
        apellido="Rodriguez",
        email="Andres@example.com",
        usuario="AndresRodriguez",
        claustro='DOCENTE',
        password="password345"
    )