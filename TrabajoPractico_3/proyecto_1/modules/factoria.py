from modules.repositorioConcreto.adhesion_concreto import AdhesionRepositorio
from modules.repositorioConcreto.usuario_concreto import UsuarioRepositorio
from modules.repositorioConcreto.reclamo_concreto import ReclamoRepositorio
from modules.repositorioConcreto.departamento_concreto import DepartamentoRepositorio
from modules.config import crear_engine
from modules.reporte.pdf import ReportePDF
from modules.reporte.html import ReporteHtml


def crear_repositorio():
    Session = crear_engine()
    repo_departamento =  DepartamentoRepositorio(Session())
    repo_usuario = UsuarioRepositorio(Session())
    repo_reclamo = ReclamoRepositorio(Session())
    repo_adhesion = AdhesionRepositorio(Session())
    return  repo_usuario, repo_reclamo, repo_departamento, repo_adhesion

def crear_reporte(tipo: str):
    if tipo == 'pdf':
        return ReportePDF()
    elif tipo == 'html':
        return ReporteHtml()
    else:
        raise ValueError(f"Tipo de reporte desconocido: {tipo}")