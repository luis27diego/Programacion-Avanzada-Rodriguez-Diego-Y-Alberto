#from modules import Estudiante
#from modules import Profesor
#from modules import Departamento

class Curso:
    def __init__(self, nombre, codigo, departamento,titular):
        self.nombre = nombre
        self.codigo = codigo
        self._estudiantes = []  # Inicializa como lista vacía
        self._profesores = []
        self.departamento = departamento  # Departamento es un atributo protegido
        self.titular = titular  # Titular es un atributo protegido

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
        return [estudiante.to_dict() for estudiante in self._estudiantes]
    
    def agregar_estudiante(self, estudiante): 
        from .Estudiante import Estudiante
        if not isinstance(estudiante, Estudiante):
            raise TypeError("El estudiante debe ser una instancia de la clase Estudiante.")
        if estudiante not in self._estudiantes:
            estudiante.agregar_curso(self)
            self._estudiantes.append(estudiante)
        else:
            raise ValueError("El estudiante ya está inscrito en el curso.")

    @property
    def profesores(self):
        return [profesor.to_dict() for profesor in self._profesores]
    
    def agregar_profesor(self, profesor):
        from .Profesor import Profesor
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        if profesor not in self._profesores:
            self._profesores.append(profesor)

    @property
    def departamento(self):
        return self._departamento

    @departamento.setter
    def departamento(self, valor):
        from .Departamento import Departamento
        if not isinstance(valor, Departamento):
            raise TypeError("El departamento debe ser una instancia de la clase Departamento.")
        self._departamento = valor
    
    @property
    def titular(self):
        return self._titular
    @titular.setter
    def titular(self, valor):
        from .Profesor import Profesor
        if not isinstance(valor, Profesor):
            raise TypeError("El titular debe ser una instancia de la clase Profesor.")
        self._titular = valor
        valor.ensena_en = self

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "codigo": self.codigo,
            "profesores": [profesor.to_dict() for profesor in self._profesores],
            "departamento": self.departamento.nombre if self.departamento else None,
            "titular": self.titular.nombre if self.titular else None
        }

    def __str__(self):
        return f"Curso: {self.nombre}, Código: {self.codigo}, Departamento: {self.departamento.nombre}"
if __name__ == "__main__":
    # Ejemplo de uso
    from modules.Departamento import Departamento
    from modules.Profesor import Profesor

    depto = Departamento("Ciencias", Profesor("Ana Gomez", 40, "12345678", "Matemáticas"))
    curso = Curso("Álgebra", "MATH101", depto)
    print(f"Curso: {curso.nombre}, Código: {curso.codigo}, Departamento: {curso.departamento.nombre}")

# python -m modules.Curso # Ejecuta el módulo Curso.py directamente para pruebas rápidas