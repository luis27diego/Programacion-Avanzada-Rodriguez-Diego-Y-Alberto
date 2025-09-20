# app.py
from flask import Flask, render_template, request, redirect, url_for

from modules.ControladorSistema import ControladorSistema


app = Flask(__name__)
app.secret_key = 'smart_belt_secret_key_2024'


# Instancia global del controlador
controlador = ControladorSistema()


# Nueva lógica: todo el flujo se maneja por rutas y recarga de página
@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = None
    error = None
    estado = controlador.obtener_estado_actual()
    #print(estado)

    # Procesar automáticamente si es GET y está corriendo
    if request.method == 'GET' and controlador.estado == "running":
        try:
            controlador.procesar_siguiente_alimento()
            estado = controlador.obtener_estado_actual()  # Actualizar estado después de procesar
        except Exception as e:
            error = str(e)

    if request.method == 'POST':
        # Iniciar proceso
        try:
            capacidad = int(request.form.get('numAlimentos', 100))
            if capacidad < 1 or capacidad > 1000:
                error = "Capacidad debe estar entre 1 y 1000"
            else:
                controlador.iniciar_proceso(capacidad)
                estado = controlador.obtener_estado_actual()
                mensaje = "Proceso iniciado correctamente"
        except Exception as e:
            error = str(e)
    return render_template('inicio.html', estado=estado, mensaje=mensaje, error=error)


# Ruta para procesar siguiente alimento
@app.route('/procesar', methods=['POST'])
def procesar():
    resultado = None
    error = None
    if controlador.estado != "running":
        error = "No se puede procesar más alimentos"
    else:
        resultado = controlador.procesar_siguiente_alimento()
    estado = controlador.obtener_estado_actual()
    return render_template('inicio.html', estado=estado, resultado=resultado, error=error)

# Ruta para resetear el sistema
@app.route('/reset', methods=['POST'])
def reset():
    global controlador
    controlador = ControladorSistema()
    estado = controlador.obtener_estado_actual()
    return render_template('inicio.html', estado=estado, mensaje="Sistema reseteado")


if __name__ == '__main__':
    app.run(debug=True, port=5000)


# Para ejecutar:
# 1. Instalar Flask: pip install flask
# 2. Ejecutar: python app.py
# 3. Abrir: http://localhost:5000