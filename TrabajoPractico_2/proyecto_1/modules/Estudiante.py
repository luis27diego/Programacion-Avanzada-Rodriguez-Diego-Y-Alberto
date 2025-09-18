from modules import Persona
from modules import Curso
from modules import Facultad

class Estudiante(Persona):
    def __init__(self, nombre, edad, dni):
        super().__init__(nombre, edad, dni)
        self._cursos = []
        self.facultades = None  # Facultades es un atributo protegido

    @property
    def cursos(self):
        return self._cursos

    @cursos.setter
    def cursos(self, valor):
        if not isinstance(valor, Curso):
            raise TypeError("Los cursos deben ser instancias de la clase Curso.")
        self._cursos.append(valor)

    @property
    def facultades(self):
        return self._facultades 
    
    @facultades.setter
    def facultades(self, valor):
        if valor is not None:
            if not isinstance(valor, Facultad):
                raise TypeError("La facultad debe ser una instancia de la clase Facultad.")

        self._facultades = valor
    
