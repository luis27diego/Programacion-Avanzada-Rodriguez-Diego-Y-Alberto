# test_sistema.py
# Ejecutar desde la carpeta proyecto_1 con: python test_sistema.py

from modules.Profesor import Profesor
from modules.Departamento import Departamento
from modules.Estudiante import Estudiante
from modules.Facultad import Facultad
from modules.Curso import Curso

def main():
    # Crear un profesor
    profesor1 = Profesor("Juan Pérez", 45, "12345678", "Matemáticas")
    print(f"Creado: {profesor1}")
    
    # Crear un departamento
    departamento_matematicas = Departamento("Departamento de Matemáticas", profesor1)
    print(f"Creado: {departamento_matematicas}")
    
    # Verificar que el profesor es director
    print(f"¿Es director? {profesor1.Es_director is not None}")
    
    # Crear un estudiante
    estudiante1 = Estudiante("María García", 20, "87654321")
    print(f"Creado: {estudiante1}")
    
    # Crear una facultad
    facultad_ciencias = Facultad("Facultad de Ciencias", "Campus Norte")
    print(f"Creada: {facultad_ciencias}")
    
    # Agregar estudiante a facultad
    facultad_ciencias.agregar_estudiante(estudiante1)
    estudiante1.facultad = facultad_ciencias
    
    # Crear un curso
    curso_calculo = Curso("Cálculo I", "MAT101", departamento_matematicas)
    print(f"Creado: {curso_calculo}")
    
    # Agregar estudiante al curso
    curso_calculo.agregar_estudiante(estudiante1)
    estudiante1.agregar_curso(curso_calculo)
    
    # Agregar profesor al curso
    curso_calculo.agregar_profesor(profesor1)
    
    print("\n--- Resumen ---")
    print(f"Estudiante {estudiante1.nombre} está inscrito en {len(estudiante1.cursos)} curso(s)")
    print(f"Curso {curso_calculo.nombre} tiene {len(curso_calculo.estudiantes)} estudiante(s)")
    print(f"Departamento {departamento_matematicas.nombre} dirigido por {departamento_matematicas.director.nombre}")

if __name__ == "__main__":
    main()