from modules.estudiante import Estudiante
class Departamento:
    def __init__(self, nombre, director):
        self.nombre = nombre
        self._profesores = []
        self._cursos = []
        self.director = director
     

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
        from modules.profesor import Profesor
        if profesor is not None and not isinstance(profesor, Profesor):
            raise TypeError("El director del departamento debe ser una instancia de la clase Profesor.")
        if profesor.departamento_dirigido is not None:
            raise ValueError("El profesor ya es director de otro departamento.")
        self._director = profesor
        self._profesores.append(profesor)
        profesor.departamento_dirigido = self

    def agregar_profesor(self, profesor):
        from modules.profesor import Profesor
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        print("*"*20, self._profesores)
        if profesor not in self._profesores:
            self._profesores.append(profesor)

    @property
    def profesores(self):
        return self._profesores

    @property
    def cursos(self):
        return self._cursos
    
    def crear_curso(self, nombre, codigo, titular):
        from modules.profesor import Profesor
        if not isinstance(titular, Profesor):
            raise TypeError("El titular debe ser una instancia de la clase Profesor.")
        from .Curso import Curso
        curso = Curso(nombre, codigo, titular)
        if curso not in self._cursos:
            self._cursos.append(curso)
            titular.agregar_departamento(self) # Asignar el departamento al profesor
            self.agregar_profesor(titular) # Agregar el profesor a la lista de profesores del departamento
        else:
            raise ValueError("El curso ya existe en el departamento.")

    def inscribir_estudiante_curso(self, estudiante, curso_str):
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
    
    def mostrar_profesores(self):
        return [profesor.nombre for profesor in self._profesores]
    def __eq__(self, other):
        if not isinstance(other, Departamento):
            return False
        return self.nombre == other.nombre #and self.director == other.director"""


if __name__ == "__main__":
    # Ejemplo de uso
    from modules.profesor import Profesor
    from modules.departamento import Departamento

    try:
        prof = Profesor("Ana Gomez", 50, "12345678", "Matemáticas")
        dept = Departamento("Ciencias", prof)
        print(f"Departamento: {dept.nombre}, Director: {dept.director}")
    except Exception as e:
        print(f"Error: {e}")


    #verificacion entre igualdad de departamentos
    prof1 = Profesor("Ana Gomez", 50, "12345678", "Matemáticas")
    prof2 = Profesor("Francisco", 50, "12345678", "Matemáticas")
    dept1 = Departamento("Ciencias", prof1)
    dept2 = Departamento("Ciencias", prof2)
    print(f"Los departamentos son iguales: {dept1 == dept2}") 

    print(f"dept1 es instancia de Departamento: {isinstance(dept1, Departamento)}")
    print(f"dept2 no es instancia de Departamento: {isinstance(dept2, Profesor)}")
  