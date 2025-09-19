# Importamos todas las clases principales para que estén disponibles
from .Persona import Persona
from .Profesor import Profesor
from .Estudiante import Estudiante
from .Departamento import Departamento
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
]