from modules.estudiante import Estudiante

class Curso:
    def __init__(self, nombre, codigo,titular):
        self.nombre = nombre
        self.codigo = codigo
        self._estudiantes = []  
        self._profesores = []
        self.titular = titular
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
        from modules.profesor import Profesor
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        if profesor not in self._profesores:
            self._profesores.append(profesor)
    
    @property
    def titular(self):
        return self._titular
    @titular.setter
    def titular(self, valor):
        from modules.profesor import Profesor
        if not isinstance(valor, Profesor):
            raise TypeError("El titular debe ser una instancia de la clase Profesor.")
        self._titular = valor
        valor.ensena_en = self

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "codigo": self.codigo,
            "profesores": [profesor.to_dict() for profesor in self._profesores],
            "titular": self.titular.nombre if self.titular else None
        }

    def __str__(self):
        return f"Curso: {self.nombre}, Código: {self.codigo}, Departamento: {self.departamento.nombre}"
    
if __name__ == "__main__":

    # Ejemplo de uso
    from modules.departamento import Departamento
    from modules.profesor import Profesor
    from modules.Curso import Curso
    prof = Profesor("Ana Gomez", 40, "12345678", "Matemáticas")
    depto = Departamento("Ciencias",prof)
    curso = Curso("Álgebra", "MATH101", prof)
    print(f"Curso: {curso.nombre}, Código: {curso.codigo}")
