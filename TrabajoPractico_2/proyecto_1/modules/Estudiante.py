from modules import Persona
#from modules import Curso
#from modules import Facultad

class Estudiante(Persona):
    def __init__(self, nombre, edad, dni):
        super().__init__(nombre, edad, dni)
        self._cursos = []
        self.facultad = None  # Facultades es un atributo protegido

    @property
    def cursos(self):
        return self._cursos

    def agregar_curso(self, curso):
        from .Curso import Curso
        if not isinstance(curso, Curso):
            raise TypeError("Los cursos deben ser instancias de la clase Curso.")
        if curso not in self._cursos:
            self._cursos.append(curso)

    @property
    def facultad(self):
        return self._facultad

    @facultad.setter
    def facultad(self, valor):
        if valor is not None:
            from .Facultad import Facultad
            if not isinstance(valor, Facultad):
                raise TypeError("La facultad debe ser una instancia de la clase Facultad.")
        self._facultad = valor
    
