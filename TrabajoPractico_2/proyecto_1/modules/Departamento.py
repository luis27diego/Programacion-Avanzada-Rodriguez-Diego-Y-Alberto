from modules import Profesor

class Departamento:
    def __init__(self, nombre, director):
        self.nombre = nombre
        self.director = director
        self.profesores = []

    
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
    def director(self, valor):  
        if not isinstance(valor, Profesor):
            raise TypeError("El director del departamento debe ser una instancia de la clase Profesor.")
        self._director = valor
        self.__actualizo_estado_director(valor)

    def agregar_profesor(self, profesor):
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        self.profesores.append(profesor)

    def __actualizo_estado_director(self, director):
        if not isinstance(director, Profesor):
            raise TypeError("El director debe ser una instancia de la clase Profesor.")
        director.Es_director = self


