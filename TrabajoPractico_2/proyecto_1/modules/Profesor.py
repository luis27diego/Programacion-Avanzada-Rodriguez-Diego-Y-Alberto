from modules.persona  import Persona
from modules.departamento import Departamento

class Profesor(Persona):
    def __init__(self, nombre, edad, dni, especialidad):
        super().__init__(nombre, edad, dni)
        self.especialidad = especialidad
        self._departamentos = []  
        self.departamento_dirigido = None  
        self.ensena_en = None

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
        if not isinstance(departamento, Departamento):
            raise TypeError("Los departamentos deben ser instancias de la clase Departamento.")
        if departamento not in self._departamentos:
            self._departamentos.append(departamento)

    @property
    def departamento_dirigido(self):
        return self._departamento_dirigido
    
    @departamento_dirigido.setter
    def departamento_dirigido(self, valor):
        if valor is not None:
            #print(id(type(valor)), '*'*50)
            #print(id(Departamento))
            if not isinstance(valor, Departamento):
            #    print(id(type(valor)), '*'*50)
            #    print(id(Departamento))
                raise TypeError("departamento_dirigido debe ser una instancia de Departamento o None.")
        self._departamento_dirigido = valor

    @property
    def ensena_en(self):
        return self._ensena_en
    
    @ensena_en.setter
    def ensena_en(self, valor):
        from modules.Curso import Curso
        if valor is not None and not isinstance(valor, Curso):
            raise TypeError("ensena_en debe ser una instancia de Curso o None.")
        self._ensena_en = valor 
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "dni": self.dni,
            "especialidad": self.especialidad,
            "departamentos": [dept.nombre for dept in self._departamentos],
            "departamento_dirigido": self.departamento_dirigido.nombre if self.departamento_dirigido else None,
            "ensena_en": self.ensena_en.nombre if self.ensena_en else None
        }

if __name__ == "__main__":
    # Ejemplo de uso
    try:
        from modules.departamento import Departamento
        from modules.profesor import Profesor
        prof = Profesor("Carlos Ruiz", 45, "87654321", "Historia")
        print(f"Nombre: {prof.nombre}, Edad: {prof.edad}, DNI: {prof.dni}, Especialidad: {prof.especialidad}")
        dept = Departamento("Humanidades", prof)

    except Exception as e:
        print(f"Error: {e}")