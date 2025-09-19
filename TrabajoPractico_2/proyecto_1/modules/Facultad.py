from modules import Departamento
from modules import Estudiante
from modules import Curso
from modules import Profesor

class Facultad:
    def __init__(self, nombre):
        self.nombre = nombre
        self.departamentos = []
        self.estudiantes = []
        self.cursos = []
        self.profesores = []

    def agregar_departamento(self, departamento):
        if not isinstance(departamento, Departamento):
            raise TypeError("El departamento debe ser una instancia de la clase Departamento.")
        self.departamentos.append(departamento)

    def agregar_estudiante(self, estudiante):
        if not isinstance(estudiante, Estudiante):
            raise TypeError("El estudiante debe ser una instancia de la clase Estudiante.")
        self.estudiantes.append(estudiante)

    def agregar_curso(self, curso):
        if not isinstance(curso, Curso):
            raise TypeError("El curso debe ser una instancia de la clase Curso.")
        self.cursos.append(curso)

    def agregar_profesor(self, profesor):
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        self.profesores.append(profesor)

