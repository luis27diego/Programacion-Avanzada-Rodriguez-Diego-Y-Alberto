from modules.persona import Persona

class Estudiante(Persona):
    def __init__(self, nombre, edad, dni):
        super().__init__(nombre, edad, dni)
        self._cursos = []

    @property
    def cursos(self):
        return self._cursos

    def agregar_curso(self, curso):
        from modules.Curso import Curso
        if not isinstance(curso, Curso):
            raise TypeError("Los cursos deben ser instancias de la clase Curso.")
        if curso not in self._cursos:
            self._cursos.append(curso)

    def cursos_anotados(self):
        return [curso.nombre for curso in self._cursos]
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "dni": self.dni,
            "cursos": [curso.to_dict().get("nombre") for curso in self._cursos],
        }
    
