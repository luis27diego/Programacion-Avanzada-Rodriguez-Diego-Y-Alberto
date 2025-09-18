
from Persona import Persona
from modules import Departamento

class Profesor(Persona):
    def __init__(self, nombre, edad, dni, especialidad):
        super().__init__(nombre, edad, dni)
        self.especialidad = especialidad
        self._departamentos = []  
        self.Es_director = False  

    @property
    def especialidad(self):
        return self._especialidad
     
    @especialidad.setter
    def especialidad(self, valor):
        if not isinstance(valor, str):
            raise TypeError("La especialidad debe ser una cadena de texto.")
        self._especialidad = valor

    @property
    def departamentos(self):
        return self._departamentos
    
    @departamentos.setter
    def departamentos(self, valor):
        if not isinstance(valor, Departamento):
            raise TypeError("Los departamentos deben ser instancias de la clase Departamento.")
        self._departamentos.append(valor)

    @property
    def Es_director(self):
        return self._Es_director
    
    @Es_director.setter
    def Es_director(self, valor):
        if not isinstance(valor,Departamento):
            raise TypeError("Es_director debe ser una instancia de Departamento.")
        self._Es_director = valor
