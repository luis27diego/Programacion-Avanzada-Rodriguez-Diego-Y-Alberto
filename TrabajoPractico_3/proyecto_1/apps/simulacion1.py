from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from modules.dominio.usuario import UsuarioDominio, UsuarioFinal, ResponsableDepartamento
from modules.dominio.reclamo import ReclamoDominio, Estado
from modules.dominio.departamento import DepartamentoDominio
from modules.dominio.reclamo import AdhesionDominio
from modules.repositorioConcreto.usuario_concreto import UsuarioRepositorio as SqlUsuarioRepositorio
from modules.repositorioConcreto.reclamo_concreto import ReclamoRepositorio as SqlReclamoRepositorio
from modules.repositorioConcreto.departamento_concreto import DepartamentoRepositorio as SqlDepartamentoRepositorio
from modules.repositorioConcreto.adhesion_concreto import AdhesionRepositorio as SqladhesionRepositorio
from modules.modelos import Base

# Configuración de la base de datos
engine = create_engine('sqlite:///data/database.db', echo=True) # <-- MODIFICADO
Session = sessionmaker(bind=engine)
session = Session()

# Crear tablas si no existen
Base.metadata.create_all(engine)

# Repositorios concretos
usuario_repo = SqlUsuarioRepositorio(session)
reclamo_repo = SqlReclamoRepositorio(session)
departamento_repo = SqlDepartamentoRepositorio(session)
adhesion_repo = SqladhesionRepositorio(session)  

# Simulación
print("Iniciando simulación a las 14:02 del 05/10/2025...")

# 1. Crear departamentos iniciales
if departamento_repo.obtener_todos_los_registros() == []:
    dept_a = DepartamentoDominio(id=1, nombre='Maestranza')
    dept_b = DepartamentoDominio(id=2, nombre='Soporte Informático')
    dept_sec = DepartamentoDominio(id=3, nombre='Secretaria Tecnica')
    departamento_repo.guardar_registro(dept_a)
    departamento_repo.guardar_registro(dept_b)
    departamento_repo.guardar_registro(dept_sec)
    print("Departamentos creados:", [d.nombre for d in departamento_repo.obtener_todos_los_registros()])

# 2. Crear usuarios
if usuario_repo.obtener_todos_los_registros() == []:
    user_final = UsuarioFinal(
        id=1, nombre='Juan', apellido='Perez', email='juan@example.com', usuario='juanp',
        claustro="ESTUDIANTE", password='hash_pass1' 
    )
    user_final2 = UsuarioFinal(
        id=2, nombre='Maria', apellido='Lopez', email='maria@example.com', usuario='marial',
        claustro="ESTUDIANTE", password='hash_pass2' 
    )

    jefe = ResponsableDepartamento(
        id=3, nombre='Ana', apellido='Gomez', email='ana@example.com', usuario='anag',
        password='hash_pass2', rol="JEFE_DEPARTAMENTO", departamento_id=1
    )
    secretario = ResponsableDepartamento(
        id=4, nombre='Carlos', apellido='Lopez', email='carlos@example.com', usuario='carlosl',
        password='hash_pass3', rol="SECRETARIO_TECNICO", departamento_id=3
    )
    usuario_repo.guardar_registro(user_final)
    usuario_repo.guardar_registro(user_final2)
    usuario_repo.guardar_registro(jefe)
    usuario_repo.guardar_registro(secretario)
    print("Usuarios creados:", [u.usuario for u in usuario_repo.obtener_todos_los_registros()])

# 3. Crear reclamos
if reclamo_repo.obtener_todos_los_registros() == []:
    reclamo1 = ReclamoDominio(
        id=1, usuario_id=1, contenido='Problema con el aula 101', timestamp=datetime.now(),
        estado=Estado.PENDIENTE, departamento_id=1
    )
    reclamo2 = ReclamoDominio(
        id=2, usuario_id=1, contenido='Falta de materiales', timestamp=datetime.now(),
        estado=Estado.PENDIENTE, departamento_id=2
    )
    reclamo_repo.guardar_registro(reclamo1)
    reclamo_repo.guardar_registro(reclamo2)
    print("Reclamos creados:", [r.contenido for r in reclamo_repo.obtener_todos_los_registros()])

# 4. Cargar usuario y agregar reclamos creados
user = usuario_repo.obtener_registro_por_filtro('id', 1)

# 5. Agregar adhesión (usuario2 adhiere a reclamo1)
adhesion = AdhesionDominio(id=None, usuario_id=2, reclamo_id=1)
adhesion_repo.guardar_registro(adhesion)
reclamo = reclamo_repo.obtener_registro_por_filtro('id', 1)
if reclamo:
    user2= usuario_repo.obtener_registro_por_filtro('id', 2)
    if user2:
        print(f"Reclamo1 tiene {reclamo.cantidad_adherentes()} adherente(s).")

# 6. Cambiar estado (solo jefe o secretario)
jefe = usuario_repo.obtener_registro_por_filtro('id', 3)
if jefe and reclamo:
    reclamo.estado = Estado.EN_PROCESO
    reclamo.tiempo_resolucion = 5  # días
    reclamo_repo.modificar_registro(reclamo)

#8  Crear usuario vacio
usuario_vacio = UsuarioFinal(
    id=None, nombre='Luis', apellido='Diego', email='luis.diego@example.com', usuario='luisd',
    claustro="ESTUDIANTE", password='hash_pass4'
)
usuario_repo.guardar_registro(usuario_vacio)

obtenido = usuario_repo.obtener_registro_por_filtro('usuario', 'luisd')

# 8. Limpiar sesión
session.close()
print("Simulación finalizada.")