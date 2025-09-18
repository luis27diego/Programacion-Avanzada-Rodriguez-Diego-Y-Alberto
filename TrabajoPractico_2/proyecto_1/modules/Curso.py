from modules import Estudiante
from modules import Profesor
from modules import Departamento

class Curso:
    def __init__(self, nombre, codigo, departamento):
        self.nombre = nombre
        self.codigo = codigo
        self._estudiantes = []  # Inicializa como lista vacía
        self._profesor = []
        self.departamento = departamento  # Departamento es un atributo protegido

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise TypeError("El nombre del curso debe ser una cadena de texto.")
        if not valor.strip():
            raise ValueError("El nombre del curso debe ser una cadena de texto no vacía.")
        self._nombre = valor.strip()

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not isinstance(valor, str):
            raise TypeError("El código del curso debe ser una cadena de texto.")
        if not valor.strip():
            raise ValueError("El código del curso debe ser una cadena de texto no vacía.")
        self._codigo = valor.strip()

    @property
    def estudiantes(self):
        return self._estudiantes
    
    @estudiantes.setter
    def agregar_estudiante(self, estudiante):
        if not isinstance(estudiante, Estudiante):
            raise TypeError("El estudiante debe ser una instancia de la clase Estudiante.")
        self._estudiantes.append(estudiante)

    @property
    def profesor(self):
        return self._profesor
    
    @profesor.setter
    def profesor(self, valor):
        if not isinstance(valor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        self._profesor = valor

    @property
    def departamento(self):
        return self._departamento

    @departamento.setter
    def departamento(self, valor):
        if not isinstance(valor, Departamento):
            raise TypeError("El departamento debe ser una instancia de la clase Departamento.")
        self._departamento = valor