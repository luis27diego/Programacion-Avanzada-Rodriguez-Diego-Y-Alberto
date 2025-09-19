#from .Profesor import Profesor

class Departamento:
    def __init__(self, nombre, director):
        self.nombre = nombre
        self.director = director
        self._profesores = []

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
        self._director = profesor
        self.__actualizo_estado_director(profesor)

    def agregar_profesor(self, profesor):
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        if profesor not in self._profesores:
            self._profesores.append(profesor)

    def __actualizo_estado_director(self, director):
        from .Profesor import Profesor
        if not isinstance(director, Profesor):
            raise TypeError("El director debe ser una instancia de la clase Profesor.")
        director.Es_director = self

if __name__ == "__main__":
    # Ejemplo de uso
    try:
        from .Profesor import Profesor
        prof = Profesor("Ana Gomez", 50, "12345678", "Matemáticas")
        dept = Departamento("Ciencias", prof)
        print(f"Departamento: {dept.nombre}, Director: {dept.director}")
    except Exception as e:
        print(f"Error: {e}")