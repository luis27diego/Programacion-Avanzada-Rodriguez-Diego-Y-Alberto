#from .Profesor import Profesor

class Departamento:
    def __init__(self, nombre, director):
        self.nombre = nombre
        self.director = director
        self._profesores = []
        self._cursos = []

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, valor):    
        if not isinstance(valor, str):
            raise TypeError("El nombre del departamento debe ser una cadena de texto.")
        if not valor.strip():
            raise ValueError("El nombre del departamento debe ser una cadena de texto no vacía.")
        self._nombre = valor.strip()

    @property
    def director(self):   
        return self._director
    @director.setter
    def director(self, profesor):  
        from .Profesor import Profesor
        if profesor is not None and not isinstance(profesor, Profesor):
            raise TypeError("El director del departamento debe ser una instancia de la clase Profesor.")
        if profesor.departamento_dirigido is not None:
            raise ValueError("El profesor ya es director de otro departamento.")
        self._director = profesor
        profesor.departamento_dirigido = self

    def agregar_profesor(self, profesor):
        from .Profesor import Profesor
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        if profesor not in self._profesores:
            self._profesores.append(profesor)

    @property
    def profesores(self):
        return self._profesores

    @property
    def cursos(self):
        return self._cursos
    
    def crear_curso(self, nombre, codigo, titular):
        from .Profesor import Profesor
        if not isinstance(titular, Profesor):
            raise TypeError("El titular debe ser una instancia de la clase Profesor.")
        from .Curso import Curso
        curso = Curso(nombre, codigo, self, titular)
        if curso not in self._cursos:
            self._cursos.append(curso)
        else:
            raise ValueError("El curso ya existe en el departamento.")

    def inscribir_estudiante_curso(self, estudiante, curso_str):
        from .Estudiante import Estudiante
        if not isinstance(estudiante, Estudiante):
            raise TypeError("El estudiante debe ser una instancia de la clase Estudiante.")
        if not isinstance(curso_str, str):
            raise TypeError("El nombre del curso debe ser una cadena de texto.")
        curso_encontrado = None
        for curso in self._cursos:
            if curso.nombre == curso_str:
                curso_encontrado = curso
                break
        
        if curso_encontrado is None:
            raise ValueError(f"El curso '{curso_str}' no existe en el departamento '{self.nombre}'.")
        
        curso_encontrado.agregar_estudiante(estudiante)
    
    def obtener_cursos(self):
        return [curso.nombre for curso in self._cursos]

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "director": self.director.nombre if self.director else None,
            "cursos": [curso.to_dict().get("nombre") for curso in self._cursos]
        }


if __name__ == "__main__":
    # Ejemplo de uso
    try:
        from .Profesor import Profesor
        prof = Profesor("Ana Gomez", 50, "12345678", "Matemáticas")
        dept = Departamento("Ciencias", prof)
        print(f"Departamento: {dept.nombre}, Director: {dept.director}")
    except Exception as e:
        print(f"Error: {e}")
