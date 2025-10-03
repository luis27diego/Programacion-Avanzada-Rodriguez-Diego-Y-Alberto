""" # Importamos todas las clases principales para que estén disponibles
from .Persona import Persona
from .profesor import Profesor
from .estudiante import Estudiante
from .departamento import Departamento
from .Facultad import Facultad
from .Curso import Curso

# Definimos qué se exporta cuando se hace "from modules import *"
__all__ = [
    'Persona',
    'Profesor', 
    'Estudiante',
    'Departamento',
    'Facultad',
    'Curso'
]  """