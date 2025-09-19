from .Persona  import Persona

class Profesor(Persona):
    def __init__(self, nombre, edad, dni, especialidad):
        super().__init__(nombre, edad, dni)
        self.especialidad = especialidad
        self._departamentos = []  
        self.Es_director = None  

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

    def agregar_departamento(self, departamento):
        from .Departamento import Departamento
        if not isinstance(departamento, Departamento):
            raise TypeError("Los departamentos deben ser instancias de la clase Departamento.")
        if departamento not in self._departamentos:
            self._departamentos.append(departamento)

    @property
    def Es_director(self):
        return self._Es_director
    
    @Es_director.setter
    def Es_director(self, valor):
        # Permitir None o instancia de Departamento
        if valor is not None:
            from .Departamento import Departamento
            if not isinstance(valor, Departamento):
                raise TypeError("Es_director debe ser una instancia de Departamento o None.")
        self._Es_director = valor

if __name__ == "__main__":
    # Ejemplo de uso
    try:
        prof = Profesor("Carlos Ruiz", 45, "87654321", "Historia")
        print(f"Nombre: {prof.nombre}, Edad: {prof.edad}, DNI: {prof.dni}, Especialidad: {prof.especialidad}")
    except Exception as e:
        print(f"Error: {e}")