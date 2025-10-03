# app.py
from flask import Flask, render_template, render_template_string, request, redirect, url_for
from modules.config import app
from modules.ControladorSistema import ControladorSistema

# Instancia global del controlador
controlador = ControladorSistema()


# Nueva lógica: todo el flujo se maneja por rutas y recarga de página
@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = None
    error = None
    estado = controlador.obtener_estado_actual()

    if request.method == 'POST':
        # Iniciar proceso y procesar hasta llenar
        try:
            capacidad = int(request.form.get('numAlimentos', 100))
            if capacidad < 1 or capacidad > 1000:
                error = "Capacidad debe estar entre 1 y 1000"
            else:
                controlador.iniciar_proceso(capacidad)
                controlador.procesar_hasta_llenar()  # Procesar todos los alimentos de una vez
                estado = controlador.obtener_estado_actual()  # Actualizar estado después de procesar
                mensaje = "Proceso completado correctamente"
        except Exception as e:
            error = str(e)

    return render_template('inicio.html', estado=estado, mensaje=mensaje, error=error)

# Ruta para resetear el sistema
@app.route('/reset', methods=['POST'])
def reset():
    global controlador
    controlador = ControladorSistema()
    estado = controlador.obtener_estado_actual()
    return render_template('inicio.html', estado=estado, mensaje="Sistema reseteado")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)