# main.py
from modules.Estudiante import Estudiante
from modules.Profesor import Profesor
from modules.Departamento import Departamento
from modules.Curso import Curso
from modules.Facultad import Facultad

# ...existing code...
def cargar_personas(facultad, archivo):
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
                    est = Estudiante(nombre, edad, dni)
                    estudiantes.append(est)
                    facultad.agregar_estudiante(est)
                elif tipo == "profesor":
                    nombre, edad, dni, esp = datos[1], int(datos[2]), datos[3], datos[4]
                    prof = Profesor(nombre, edad, dni, esp)
                    profesores.append(prof)
                    facultad.agregar_profesor(prof)
    except FileNotFoundError:
        print("⚠ No se encontró el archivo, se continuará sin carga automática.")
    return estudiantes, profesores
# ...existing code...

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
    facultad = Facultad("FIUNER")
    estudiantes, profesores = cargar_personas(facultad,"data/personas.txt")
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
            facultad.agregar_profesor(prof)
            print(f"✅ Profesor {nombre} contratado.")

        elif opcion == "3":
            nombre = input("Nombre del departamento: ")
            print("Seleccione director:")
            for i, p in enumerate(facultad.profesores, 1):
                print(f"{i} - {p.nombre} ({p.especialidad})")
            idx = int(input("Opción: ")) - 1
            if 0 <= idx < len(facultad.profesores):
                director = facultad.profesores[idx]
                if director.Es_director is not None:
                    print("⚠ El profesor ya es director de otro departamento.")
                    continue
                dept = Departamento(nombre, director)
                departamentos.append(dept)
                facultad.agregar_departamento(dept)
                print(f"✅ Departamento {nombre} creado con director {director.nombre}.")
                print("📋 Departamentos:")
                for d in facultad.departamentos: # o podríamos usar
                    print(f"- {d.nombre}, Director: {d.director.nombre}") #usar facultad.departamentos
            else:
                print("❌ Opción inválida.")

        elif opcion == "4":
            if not facultad.departamentos:
                print("⚠ Primero debe crear un departamento.")
                continue
            print("Seleccione departamento:")
            for i, d in enumerate(facultad.departamentos, 1):
                print(f"{i} - {d.nombre}")
            idx_depto = int(input("Opción: ")) - 1
            if 0 <= idx_depto < len(facultad.departamentos):
                dept = facultad.departamentos[idx_depto]
                nombre = input("Nombre del curso: ")
                codigo = input("Código: ")
                print("Seleccione titular:")
                for i, p in enumerate(facultad.profesores, 1): # Podriamos guardar en facultad y recorrer esa lista o los profesores del departamento seleccionado
                    print(f"{i} - {p.nombre} ({p.especialidad})")
                idx_prof = int(input("Opción: ")) - 1
                if 0 <= idx_prof < len(facultad.profesores):
                    titular = facultad.profesores[idx_prof]
                    curso = Curso(nombre, codigo, dept)
                    curso.agregar_profesor(titular)
                    cursos.append(curso)
                    facultad.agregar_curso(curso)
                    dept.agregar_curso(curso)
                    print(f"✅ Curso {nombre} creado en {dept.nombre}.")
                    print("📚 Cursos en el departamento:")
                    for c in dept.cursos:
                        print(f"- {c.nombre} ({c.codigo}) Titular: {c.profesor[0].nombre}")
                else:
                    print("❌ Profesor inválido.")

        elif opcion == "5":
            if not facultad.estudiantes:
                print("⚠ No hay estudiantes inscritos.")
                continue
            if not facultad.cursos:
                print("⚠ No hay cursos disponibles.")
                continue
            print("Seleccione estudiante:")
            for i, e in enumerate(facultad.estudiantes, 1):
                print(f"{i} - {e.nombre}")
            idx_est = int(input("Opción: ")) - 1
            print("Seleccione curso:")
            for i, c in enumerate(facultad.cursos, 1):
                print(f"{i} - {c.nombre}")
            idx_curso = int(input("Opción: ")) - 1
            if 0 <= idx_est < len(facultad.estudiantes) and 0 <= idx_curso < len(facultad.cursos):
                est = facultad.estudiantes[idx_est]
                curso = facultad.cursos[idx_curso]
                if curso in est.cursos:
                    print("⚠ El estudiante ya está inscrito en este curso.")
                    continue
                curso.agregar_estudiante(est)
                est.agregar_curso(curso)
                print(f"✅ {est.nombre} inscrito en {curso.nombre}. {est.cursos_anotados()}")
            else:
                print("❌ Opción inválida.")

        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            break

        elif opcion == "7":  
            print("📋 Listado de estudiantes:")
            for e in facultad.estudiantes:
                print(f"- {e.nombre}, Edad: {e.edad}, DNI: {e.dni}, Cursos: {[c.nombre for c in e.cursos]}")

        else:
            print("❌ Opción inválida.")
