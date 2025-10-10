from modules.departamento import Departamento
from modules.estudiante import Estudiante
# modules/Facultad.py
class Facultad:
    def __init__(self, nombre):
        self.nombre = nombre
        self._departamentos = []
        self._estudiantes = []
        self._profesores = []

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
    
    def departamentos_dict(self):
        return [dept.to_dict() for dept in self._departamentos]

    def crear_departamento(self, nombre,director_idx):
        director = self._profesores[director_idx]
        departamento = Departamento(nombre, director)
        if departamento not in self._departamentos:
            self._departamentos.append(departamento)
        else:
            raise ValueError("El departamento ya existe en la facultad.")

    @property
    def estudiantes(self):
        return self._estudiantes
    
    def estudiantes_dict(self):
        return [estudiante.to_dict() for estudiante in self._estudiantes]

    def agregar_estudiante(self, estudiante):
        if not isinstance(estudiante, Estudiante):
            raise TypeError("El estudiante debe ser una instancia de la clase Estudiante.")
        if estudiante not in self._estudiantes:
            self._estudiantes.append(estudiante)

    @property
    def profesores(self):
        return self._profesores
    
    def profesores_dict(self):
        return [profesor.to_dict() for profesor in self._profesores]
    
    def agregar_profesor(self, profesor):
        from .profesor import Profesor
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        if profesor not in self._profesores:
            self._profesores.append(profesor)
        return len(self._profesores) - 1
    
    def obtener_idx_profesor(self, profesor):
        if profesor in self._profesores:
            return self._profesores.index(profesor)
        else:
            raise ValueError("El profesor no pertenece a la facultad.")
    



    def crear_curso(self, nombre,codigo,departamento_idx,titular_idx):
        if not isinstance(departamento_idx, int) or not (0 <= departamento_idx < len(self._departamentos)):
            raise IndexError("Índice de departamento fuera de rango.")
        if not isinstance(titular_idx, int) or not (0 <= titular_idx < len(self._profesores)):
            raise IndexError("Índice de titular fuera de rango.")
        departamento = self._departamentos[departamento_idx]
        titular = self._profesores[titular_idx]
        if titular.ensena_en is not None:
            raise ValueError("El profesor ya es titular de otro curso.")
        departamento.crear_curso(nombre, codigo, titular)

    def inscribir_estudiante_curso(self, estudiante_idx, departamento_idx, curso_str):
        if not isinstance(estudiante_idx, int) or not (0 <= estudiante_idx < len(self._estudiantes)):
            raise IndexError("Índice de estudiante fuera de rango.")
        estudiante = self._estudiantes[estudiante_idx]
        if not isinstance(departamento_idx, int) or not (0 <= departamento_idx < len(self._departamentos)):
            raise IndexError("Índice de departamento fuera de rango.")
        departamento = self._departamentos[departamento_idx]
        departamento.inscribir_estudiante_curso(estudiante, curso_str)

    def cursos_departamento_idx(self): #Devuelve los cursos con el idx del departamento al que pertenecen (Matematica,0),(Fisica,0),(Historia,1)...
        lista = []
        if not self._departamentos:
            raise ValueError("No hay departamentos en la facultad. Por lo tanto, no hay cursos.")
        for idx, departamento in enumerate(self._departamentos):
            departamento_cursos = departamento.obtener_cursos()
            for curso in departamento_cursos:
                lista.append((curso, idx))
        return lista
    

    def asociar_profe_depto(self, profesor_idx, departamento_idx):
        if not isinstance(profesor_idx, int) or not (0 <= profesor_idx < len(self._profesores)):
            raise IndexError("Índice de profesor fuera de rango.")
        profesor = self._profesores[profesor_idx]
        if not isinstance(departamento_idx, int) or not (0 <= departamento_idx < len(self._departamentos)):
            raise IndexError("Índice de departamento fuera de rango.")
        departamento = self._departamentos[departamento_idx]
        departamento.agregar_profesor(profesor)
        profesor.agregar_departamento(departamento)

    def __str__(self):
        return f"Facultad: {self.nombre}"