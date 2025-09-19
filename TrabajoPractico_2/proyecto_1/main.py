# main.py
from modules.Estudiante import Estudiante
from modules.Profesor import Profesor
from modules.Departamento import Departamento
from modules.Curso import Curso
from modules.Facultad import Facultad

def cargar_personas(archivo):
    estudiantes = []
    profesores = []
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) == 0:
                    continue
                tipo = datos[0].lower()
                if tipo == "estudiante":
                    nombre, edad, dni = datos[1], int(datos[2]), datos[3]
                    estudiantes.append(Estudiante(nombre, edad, dni))
                elif tipo == "profesor":
                    nombre, edad, dni, esp = datos[1], int(datos[2]), datos[3], datos[4]
                    profesores.append(Profesor(nombre, edad, dni, esp))
    except FileNotFoundError:
        print("⚠ No se encontró el archivo, se continuará sin carga automática.")
    return estudiantes, profesores

def menu():
    print("\n##########################################")
    print("#  Sistema de Información Universitaria  #")
    print("##########################################")
    print("Elige una opción")
    print("1 - Inscribir alumno")
    print("2 - Contratar profesor")
    print("3 - Crear departamento nuevo")
    print("4 - Crear curso nuevo")
    print("5 - Inscribir estudiante a un curso")
    print("6 - Salir")

if __name__ == "__main__":
    # Inicialización
    facultad = Facultad("FIUNER", "Paraná, Entre Ríos")
    estudiantes, profesores = cargar_personas("personas.txt")
    departamentos = []
    cursos = []

    while True:
        menu()
        opcion = input("Opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            dni = input("DNI: ")
            est = Estudiante(nombre, edad, dni)
            estudiantes.append(est)
            facultad.agregar_estudiante(est)
            print(f"✅ Estudiante {nombre} inscrito.")

        elif opcion == "2":
            nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            dni = input("DNI: ")
            esp = input("Especialidad: ")
            prof = Profesor(nombre, edad, dni, esp)
            profesores.append(prof)
            print(f"✅ Profesor {nombre} contratado.")

        elif opcion == "3":
            nombre = input("Nombre del departamento: ")
            print("Seleccione director:")
            for i, p in enumerate(profesores, 1):
                print(f"{i} - {p.nombre} ({p.especialidad})")
            idx = int(input("Opción: ")) - 1
            if 0 <= idx < len(profesores):
                director = profesores[idx]
                dept = Departamento(nombre, director)
                departamentos.append(dept)
                facultad.agregar_departamento(dept)
                print(f"✅ Departamento {nombre} creado con director {director.nombre}.")
                print("📋 Departamentos:")
                for d in departamentos:
                    print(f"- {d.nombre}, Director: {d.director.nombre}") #usar facultad.departamentos
            else:
                print("❌ Opción inválida.")

        elif opcion == "4":
            if not departamentos:
                print("⚠ Primero debe crear un departamento.")
                continue
            print("Seleccione departamento:")
            for i, d in enumerate(departamentos, 1):
                print(f"{i} - {d.nombre}")
            idx_depto = int(input("Opción: ")) - 1
            if 0 <= idx_depto < len(departamentos):
                dept = departamentos[idx_depto]
                nombre = input("Nombre del curso: ")
                codigo = input("Código: ")
                print("Seleccione titular:")
                for i, p in enumerate(profesores, 1): # Podriamos guardar en facultad y recorrer esa lista o los profesores del departamento seleccionado
                    print(f"{i} - {p.nombre} ({p.especialidad})")
                idx_prof = int(input("Opción: ")) - 1
                if 0 <= idx_prof < len(profesores):
                    titular = profesores[idx_prof]
                    curso = Curso(nombre, codigo, dept)
                    curso.agregar_profesor(titular)
                    cursos.append(curso)
                    print(f"✅ Curso {nombre} creado en {dept.nombre}.")
                    print("📚 Cursos en el departamento:")
                    for c in cursos:
                        if c.departamento == dept:
                            print(f"- {c.nombre} ({c.codigo}) Titular: {c.profesor[0].nombre}")
                else:
                    print("❌ Profesor inválido.")

        elif opcion == "5":
            if not estudiantes or not cursos:
                print("⚠ No hay estudiantes o cursos disponibles.")
                continue
            print("Seleccione estudiante:")
            for i, e in enumerate(estudiantes, 1):
                print(f"{i} - {e.nombre}")
            idx_est = int(input("Opción: ")) - 1
            print("Seleccione curso:")
            for i, c in enumerate(cursos, 1):
                print(f"{i} - {c.nombre}")
            idx_curso = int(input("Opción: ")) - 1
            if 0 <= idx_est < len(estudiantes) and 0 <= idx_curso < len(cursos):
                est = estudiantes[idx_est]
                curso = cursos[idx_curso]
                if curso in est.cursos:
                    print("⚠ El estudiante ya está inscrito en este curso.")
                    continue
                curso.agregar_estudiante(est)
                est.agregar_curso(curso)
                print(f"✅ {est.nombre} inscrito en {curso.nombre}. {est.cursos}")
            else:
                print("❌ Opción inválida.")

        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            break

        else:
            print("❌ Opción inválida.")
