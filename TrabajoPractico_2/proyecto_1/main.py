# main.py
from modules.estudiante import Estudiante
from modules.profesor import Profesor
from modules.Facultad import Facultad

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
    print("7 - Listar estudiantes")
    print("8 - Listar profesores")

if __name__ == "__main__":
    # Inicialización
    facultad = Facultad("FIUNER")
    estudiantes, profesores = cargar_personas(facultad,"data/personas.txt")

    while True:
        menu()
        opcion = input("Opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            dni = input("DNI: ")
            est = Estudiante(nombre, edad, dni)
            facultad.agregar_estudiante(est)
            estudiantes.append(est)
            print(f"✅ Estudiante {nombre} inscrito.")

        elif opcion == "2":
            nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            dni = input("DNI: ")
            esp = input("Especialidad: ")
            prof = Profesor(nombre, edad, dni, esp)
            idx_profe =facultad.agregar_profesor(prof)

            prof.facultad = facultad

            # listar departamentos disponibles
            departamentos = facultad.departamentos_dict() 
            for i, d in enumerate(departamentos, 1):
                print(f"{i} - {d['nombre']}")

            # solicitar que selccione
            idx_depto = int(input("Seleccione departamento (o presione Enter para omitir): ")) - 1
            

            # agregar el profesor el departamento
            # profesor tiene que conocer el departamento asignado 
            facultad.asociar_profe_depto(idx_profe, idx_depto)
            print(f"✅ Profesor {nombre} contratado.")

        # Crear departamento nuevo
        elif opcion == "3":
            nombre = input("Nombre del departamento: ")
            print("Seleccione director:")
            for i, p in enumerate(facultad.profesores_dict(), 1):
                print(f"{i} - {p['nombre']} ({p['especialidad']})")
            idx = int(input("Opción: ")) - 1
            if 0 <= idx < len(facultad.profesores_dict()):
                director = facultad.profesores_dict()[idx]
                print(director)
                if director['departamento_dirigido'] is not None:
                    print("⚠ El profesor ya es director de otro departamento.")
                    continue
                facultad.crear_departamento(nombre, idx)
                print(f"✅ Departamento {nombre} creado con director {director['nombre']}.")
                print("📋 Departamentos:")
                for d in facultad.departamentos_dict():
                    print(f"- {d['nombre']}, Director: {d['director']}")
            else:
                print("❌ Opción inválida.")

        elif opcion == "4":
            if not facultad.departamentos_dict():
                print("⚠ Primero debe crear un departamento.")
                continue
            print("Seleccione departamento:")
            for i, d in enumerate(facultad.departamentos_dict(), 1):
                print(f"{i} - {d['nombre']}")
            idx_depto = int(input("Opción: ")) - 1
            if 0 <= idx_depto < len(facultad.departamentos):
                #dept = facultad.departamentos[idx_depto]
                nombre = input("Nombre del curso: ")
                codigo = input("Código: ")
                print("Seleccione titular:")
                for i, p in enumerate(facultad.profesores_dict(), 1): # Podriamos guardar en facultad y recorrer esa lista o los profesores del departamento seleccionado
                    print(f"{i} - {p['nombre']} ({p['especialidad']})")
                idx_prof = int(input("Opción: ")) - 1
                if 0 <= idx_prof < len(facultad.profesores):
                    try:
                        facultad.crear_curso(nombre, codigo, idx_depto, idx_prof)
                    except (ValueError) as e:
                        print(f"Error al crear curso: {e}")
                        continue
                    # Mostrar detalles del curso creado
                    departamento = facultad.departamentos_dict()[idx_depto]
                    print(f"✅ Curso {nombre} creado en {departamento['nombre']}.")
                    #Mostrar cursos del departamento
                    print("📚 Cursos en el departamento:")
                    for c in departamento.get("cursos", []):
                        print(f"- {c}")
                else:
                    print("❌ Profesor inválido.")

        elif opcion == "5":
            if not facultad.estudiantes_dict():
                print("⚠ No hay estudiantes inscritos.")
                continue
            if not facultad.cursos_departamento_idx():
                print("⚠ No hay cursos disponibles.")
                continue
            print("Seleccione estudiante:")
            for i, e in enumerate(facultad.estudiantes_dict(), 1):
                print(f"{i} - {e['nombre']}")
            idx_est = int(input("Opción: ")) - 1
            print("Seleccione curso:")
            for i, (c, idx) in enumerate(facultad.cursos_departamento_idx(), 1):
                print(f"{i} - {c}")
            idx_curso = int(input("Opción: ")) - 1
            datos = facultad.cursos_departamento_idx()[idx_curso]
            if 0 <= idx_est < len(facultad.estudiantes_dict()) and 0 <= idx_curso < len(facultad.cursos_departamento_idx()):
                #est = facultad.estudiantes_dict()[idx_est]
                try:
                    facultad.inscribir_estudiante_curso(idx_est, datos[1], datos[0])
                    est_actualizado = facultad.estudiantes_dict()[idx_est]
                    print(f"✅ {est_actualizado['nombre']} {est_actualizado['cursos']}")
                except Exception as e:
                    print(f"Error al inscribir estudiante: {e}")
                    continue
            else:
                print("❌ Opción inválida.")

        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            break

        elif opcion == "7":  
            print("📋 Listado de estudiantes:")
            for e in facultad.estudiantes_dict():
                print(f"- {e['nombre']}, Edad: {e['edad']}, DNI: {e['dni']}, Cursos: {e['cursos']}")

        elif opcion == "8":
            print("📋 Listado de profesores:")
            for p in facultad.profesores_dict():
                print(p)
                #depts = [d['nombre'] for d in p['departamentos']]
                #dir_dept = p['departamento_dirigido'] if p['departamento_dirigido'] else "Ninguno"
                #print(f"- {p['nombre']}, Edad: {p['edad']}, DNI: {p['dni']}, Especialidad: {p['especialidad']}, Departamentos: {depts}, Director de: {dir_dept}, Enseña en: {p['ensena_en'] if p['ensena_en'] else 'Ninguno'}  ")

        else:
            print("❌ Opción inválida.")
