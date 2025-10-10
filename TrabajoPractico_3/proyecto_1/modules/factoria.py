from modules.repositorioConcreto.usuario_concreto import UsuarioRepositorio
from modules.repositorioConcreto.reclamo_concreto import ReclamoRepositorio
from modules.repositorioConcreto.departamento_concreto import DepartamentoRepositorio
from modules.config import crear_engine

def crear_repositorio():
    Session = crear_engine()
    repo_departamento =  DepartamentoRepositorio(Session())
    repo_usuario = UsuarioRepositorio(Session())
    repo_reclamo = ReclamoRepositorio(Session())
    return  repo_usuario, repo_reclamo, repo_departamento