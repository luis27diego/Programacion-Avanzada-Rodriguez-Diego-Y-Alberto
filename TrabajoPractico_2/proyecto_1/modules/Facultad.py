# modules/Facultad.py
class Facultad:
    def __init__(self, nombre):
        self.nombre = nombre
        self._departamentos = []
        self._estudiantes = []

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise TypeError("El nombre de la facultad debe ser una cadena de texto.")
        if not valor.strip():
            raise ValueError("El nombre de la facultad debe ser una cadena de texto no vacía.")
        self._nombre = valor.strip()


    @property
    def departamentos(self):
        return self._departamentos

    def agregar_departamento(self, departamento):
        from .Departamento import Departamento
        if not isinstance(departamento, Departamento):
            raise TypeError("El departamento debe ser una instancia de la clase Departamento.")
        if departamento not in self._departamentos:
            self._departamentos.append(departamento)

    @property
    def estudiantes(self):
        return self._estudiantes

    def agregar_estudiante(self, estudiante):
        from .Estudiante import Estudiante
        if not isinstance(estudiante, Estudiante):
            raise TypeError("El estudiante debe ser una instancia de la clase Estudiante.")
        if estudiante not in self._estudiantes:
            self._estudiantes.append(estudiante)
            
    def __str__(self):
        return f"Facultad: {self.nombre}, Ubicación: {self.ubicacion}"