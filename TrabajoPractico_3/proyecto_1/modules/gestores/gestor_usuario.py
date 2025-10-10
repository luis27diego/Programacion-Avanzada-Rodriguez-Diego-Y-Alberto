import pickle
from typing import List, Optional
from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from modules.dominio.usuario import Claustro, Estado, Rol, UsuarioDominio
from modules.dominio.reclamo import ReclamoDominio
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class GestorDeUsuarios:
    def __init__(self, usuario_repositorio: RepositorioAbstracto, reclamo_repositorio: RepositorioAbstracto, clasificador):
        """
        Inicializa el gestor con una instancia del repositorio.
        :param repositorio: Implementación concreta de RepositorioAbstracto (UsuarioRepositorio).
        """
        self.usuario_repositorio = usuario_repositorio
        self.reclamo_repositorio = reclamo_repositorio
        self.mapeo_etiquetas = {
            "soporte informático": 1,
            "maestranza": 2,
            "secretaría técnica": 3
        }
        self.clasificador = clasificador


    def crear_usuario(self, nombre: str, apellido: str, email: str, usuario: str, password: str, claustro: Claustro, rol: Rol) -> UsuarioDominio:
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
        if self.obtener_usuario_por_filtro('email', email):
            raise ValueError("El email ya está registrado.")
        if self.obtener_usuario_por_filtro('usuario', usuario):
            raise ValueError("El nombre de usuario ya está registrado.")
        
        try:
            usuario = UsuarioDominio(
                id=None,
                nombre=nombre,
                apellido=apellido,
                email=email,
                usuario=usuario,
                password=password,
                claustro=claustro,
                rol=rol
            )
            self.usuario_repositorio.guardar_registro(usuario)
            return self.obtener_usuario_por_filtro('email', email)  # Retorna el usuario con ID
        except IntegrityError as e:
            raise ValueError(f"Error al crear el usuario: {str(e)}")

    def crear_reclamo_para_usuario(self, id_usuario: int, contenido: str, estado: Estado = Estado.PENDIENTE, tiempo_resolucion: Optional[int] = None) -> ReclamoDominio:
        """
        Permite que un usuario cree un reclamo.
        :param id_usuario: ID del usuario que crea el reclamo.
        :param contenido: Contenido del reclamo.
        :param estado: Estado inicial (default: "pendiente").
        :param tiempo_resolucion: Tiempo estimado de resolución (opcional).
        :return: El reclamo creado.
        :raises ValueError: Si el usuario no existe, no tiene permiso, o datos inválidos.
        """
        usuario = self.obtener_usuario_por_filtro('id', id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe.")
        
        # Validaciones de negocio
        if not contenido:
            raise ValueError("El contenido del reclamo no puede estar vacío.")
        
        # Clasificar el departamento (devuelve etiqueta)
        etiqueta_departamento = self.clasificador.clasificar([contenido])
        etiqueta_departamento = etiqueta_departamento[0]
        departamento_id = self.mapeo_etiquetas.get(etiqueta_departamento)
        if not departamento_id:
            raise ValueError(f"Departamento no válido: {etiqueta_departamento}")
        
        # Crear el objeto de dominio
        reclamo = ReclamoDominio(
            usuario_id=id_usuario,
            contenido=contenido,
            timestamp=datetime.now(),
            estado=estado,
            departamento_id=departamento_id,
        )
        try:
            # Guardar y obtener el reclamo creado con su ID
            reclamo_creado = self.reclamo_repositorio.guardar_registro(reclamo)
            # Agregar al usuario en memoria (si es necesario)
            usuario.agregar_reclamo_creado(reclamo_creado)
            return reclamo_creado
        except IntegrityError as e:
            raise ValueError(f"Error al crear el reclamo: {str(e)}")

    def obtener_todos_los_usuarios(self) -> List[UsuarioDominio]:
        """
        Obtiene todos los usuarios del repositorio.
        :return: Lista de objetos UsuarioDominio.
        """
        return self.usuario_repositorio.obtener_todos_los_registros()

    def modificar_usuario(self, id: int, nombre: str, apellido: str, email: str, usuario: str, password: str, claustro: Claustro, rol: Rol) -> UsuarioDominio:
        """
        Modifica un usuario existente.
        :param usuario_modificado: Objeto UsuarioDominio con los cambios.
        :return: El usuario modificado.
        :raises ValueError: Si el usuario no existe o los datos son inválidos.
        """
        if id is None:
            raise ValueError("El usuario debe tener un ID para modificarlo.")
        
        # Verificar que el usuario existe
        usuario_actual = self.obtener_usuario_por_filtro('id', id)
        if not usuario_actual:
            raise ValueError("El usuario no existe.")
        
        # Validar unicidad de email y usuario (si cambiaron)
        if email != usuario_actual.email:
            if self.obtener_usuario_por_filtro('email', email):
                raise ValueError("El email ya está registrado.")
        if usuario != usuario_actual.usuario:
            if self.obtener_usuario_por_filtro('usuario', usuario):
                raise ValueError("El nombre de usuario ya está registrado.")
        
        try:
            usuario_modificado = UsuarioDominio(
                id=id,
                nombre=nombre,
                apellido=apellido,
                email=email,
                usuario=usuario,
                password=password,
                claustro=claustro,
                rol=rol
            )
            self.usuario_repositorio.modificar_registro(usuario_modificado)
            return self.obtener_usuario_por_filtro('id', usuario_modificado.id)
        except IntegrityError as e:
            raise ValueError(f"Error al modificar el usuario: {str(e)}")

    def obtener_usuario_por_filtro(self, filtro: str, valor: any) -> Optional[UsuarioDominio]:
        """
        Obtiene un usuario basado en un filtro (ej: 'id', 'email', 'usuario').
        :param filtro: Nombre del campo para filtrar.
        :param valor: Valor del filtro.
        :return: Objeto UsuarioDominio o None si no existe.
        """
        valid_filters = ['id', 'email', 'usuario']
        if filtro not in valid_filters:
            raise ValueError(f"Filtro inválido. Use: {valid_filters}")
        return self.usuario_repositorio.obtener_registro_por_filtro(filtro, valor)

    def eliminar_usuario(self, id: int) -> bool:
        """
        Elimina un usuario por ID.
        :param id: ID del usuario a eliminar.
        :return: True si se eliminó exitosamente.
        :raises ValueError: Si el usuario no existe.
        """
        if not self.obtener_usuario_por_filtro('id', id):
            raise ValueError("El usuario no existe.")
        try:
            self.usuario_repositorio.eliminar_registro(id)
            return True
        except IntegrityError as e:
            raise ValueError(f"Error al eliminar el usuario: {str(e)}")

    def adherir_usuario_a_reclamo(self, id_usuario: int, id_reclamo: int) -> None:
        """
        Crea una adhesión entre un usuario y un reclamo.
        :param id_usuario: ID del usuario.
        :param id_reclamo: ID del reclamo.
        :raises ValueError: Si el usuario o reclamo no existen, o si ya está adherido.
        """
        usuario = self.obtener_usuario_por_filtro('id', id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe.")
        
        # Verificar si el reclamo existe (puedes extender el repositorio para incluir esta validación)
        # Aquí asumimos que el repositorio lanza una excepción si la adhesión falla
        try:
            self.usuario_repositorio.crear_relacion(id_usuario, id_reclamo, 'adhesion')
        except IntegrityError as e:
            raise ValueError(f"Error al adherir al reclamo: {str(e)}")

    def autenticar_usuario(self, usuario: str, password: str) -> Optional[UsuarioDominio]:
        """
        Autentica un usuario por nombre de usuario y contraseña.
        :param usuario: Nombre de usuario.
        :param password: Contraseña (sin hashear por simplicidad; usa bcrypt en producción).
        :return: Objeto UsuarioDominio o None si las credenciales son inválidas.
        """
        usuario_dominio = self.obtener_usuario_por_filtro('usuario', usuario)
        if usuario_dominio and usuario_dominio.password == password:  # En producción, usa hashing
            return usuario_dominio
        raise ValueError("Credenciales inválidas.")

    def obtener_reclamos_creados_por_usuario(self, id_usuario: int) -> List[ReclamoDominio]:
        """
        Obtiene los reclamos creados por un usuario.
        :param id_usuario: ID del usuario.
        :return: Lista de ReclamoDominio.
        """
        usuario = self.obtener_usuario_por_filtro('id', id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe.")
        return usuario.obtener_reclamos_creados()  

    def obtener_reclamos_adheridos_por_usuario(self, id_usuario: int) -> List[ReclamoDominio]:
        """
        Obtiene los reclamos a los que un usuario se adhirió.
        :param id_usuario: ID del usuario.
        :return: Lista de ReclamoDominio.
        """
        usuario = self.obtener_usuario_por_filtro('id', id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe.")
        return usuario.obtener_reclamos_adheridos() 
    
if __name__ == "__main__":
    from modules.factoria import crear_repositorio
    usuario_repo, reclamo_repo, departamento_repo = crear_repositorio()
    with open('../../data/claims_clf.pkl', 'rb') as archivo:
        clf = pickle.load(archivo)

    
    gestor = GestorDeUsuarios(usuario_repo, reclamo_repo, clf)



    usuario_creado = gestor.crear_usuario(
        nombre="Andres",
        apellido="Rodriguez",
        email="Andres@example.com",
        usuario="AndresRodriguez",
        claustro=Claustro.ESTUDIANTE,
        password="password345",
        rol=Rol.USUARIO_FINAL)
    print(f"Usuario creado con ID: {usuario_creado.id}")

    gestor.modificar_usuario(
        id=usuario_creado.id,
        nombre="Juan",
        apellido="Rodriguez",
        email="Andres@example.com",
        usuario="AndresRodriguez",
        claustro=Claustro.DOCENTE,
        password="password345",
        rol=Rol.USUARIO_FINAL
    )