# server.py - Solución con sesiones de Flask
from flask import render_template, request, redirect, url_for, flash, session
from modules.config import app
from modules.validaciones import validar_parametros
from modules.TriviaGame import TriviaGame
from modules.GameManager import GameManager
from modules.GameHistoria import HistorialJuego
from modules.GraficosProcesadorData import GraficosProcesadorData
from modules.GeneraciondDeGraficos import grafico_lineas, grafico_circular
from modules.pdfgenerador import generar_pdf
  
app.secret_key = '1234'

# Instancias globales que NO dependen del estado del juego
trivia_game = TriviaGame()
game_history = HistorialJuego()

def obtener_manager_usuario():
    """
    Obtiene o crea un GameManager específico para el usuario actual.
    Cada sesión tiene su propio GameManager almacenado en la sesión.
    """
    if 'game_manager_id' not in session:
        # Crear un nuevo GameManager para esta sesión
        session['game_manager_id'] = True
        session['game_data'] = {
            'usuario': None,
            'num_frases': 0,
            'aciertos': 0,
            'preguntas_hechas': [],
            'pregunta_actual': None,
            'tiempo_inicio': "",
            'tiempo_inicioSeg': 0
        }
    
    # Crear GameManager y restaurar su estado desde la sesión
    game_manager = GameManager()
    game_data = session['game_data']
    
    game_manager.usuario = game_data['usuario']
    game_manager.num_frases = game_data['num_frases']
    game_manager.aciertos = game_data['aciertos']
    game_manager.preguntas_hechas = game_data['preguntas_hechas']
    game_manager.pregunta_actual = game_data['pregunta_actual']
    game_manager.tiempo_inicio = game_data['tiempo_inicio']
    game_manager.tiempo_inicioSeg = game_data['tiempo_inicioSeg']
    
    return game_manager

def guardar_estado_game_manager(game_manager):
    """
    Guarda el estado del GameManager en la sesión.
    """
    session['game_data'] = {
        'usuario': game_manager.usuario,
        'num_frases': game_manager.num_frases,
        'aciertos': game_manager.aciertos,
        'preguntas_hechas': game_manager.preguntas_hechas,
        'pregunta_actual': game_manager.pregunta_actual,
        'tiempo_inicio': game_manager.tiempo_inicio,
        'tiempo_inicioSeg': game_manager.tiempo_inicioSeg
    }

def limpiar_sesion_usuario():
    """
    Limpia los datos del juego de la sesión del usuario.
    """
    session.pop('game_manager_id', None)
    session.pop('game_data', None)

# Página de inicio
@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("inicio.html")

@app.route("/jugar", methods=["POST"])
def jugar():
    """Ruta que inicia el juego de la trivia."""
    ok, data = validar_parametros(
        request.form.get("nombre"),
        request.form.get("num_frases")
    )
    if not ok:
        flash(data)
        return redirect(url_for("home"))
    
    # Obtener GameManager específico para este usuario
    game_manager = obtener_manager_usuario()
    
    # Iniciar el juego
    game_manager.iniciar_juego(data['nombre'], data['n'])
    
    # Guardar el estado en la sesión
    guardar_estado_game_manager(game_manager)
    
    return redirect(url_for("jugar_pregunta"))

@app.route("/jugar_pregunta", methods=["GET", "POST"])
def jugar_pregunta():
    """Ruta para cada pregunta del juego."""
    # Obtener GameManager específico para este usuario
    game_manager = obtener_manager_usuario()
    
    # Verificar si hay una sesión de juego activa
    if game_manager.obtener_usuario() is None:
        return redirect(url_for("home"))

    if request.method == "POST":
        respuesta_usuario = request.form.get('opcion')
        mensaje, categoria = game_manager.verificar_respuesta_y_actualizar_sesion(respuesta_usuario)
        flash(mensaje, categoria)
        
        # Guardar el estado actualizado
        guardar_estado_game_manager(game_manager)

        # Si el juego ha terminado después de esta respuesta
        if game_manager.juego_terminado():
            sessionterminada = game_manager.obtener_resultados_finales()
            game_history.agregar_juego(sessionterminada)
            return redirect(url_for("mostrar_resultado_final"))
        else:
            return redirect(url_for("jugar_pregunta"))
    
    else:
        # Lógica para mostrar la siguiente pregunta
        pregunta = game_manager.obtener_pregunta_nueva()
        
        # Guardar el estado actualizado (incluye la nueva pregunta)
        guardar_estado_game_manager(game_manager)
        
        return render_template("jugar_pregunta.html", pregunta=pregunta)

@app.route("/mostrar_resultado_final")
def mostrar_resultado_final():
    # Obtener GameManager específico para este usuario
    game_manager = obtener_manager_usuario()
    
    if game_manager.obtener_usuario() is None:
        return redirect(url_for("home"))  

    resultados = game_manager.obtener_resultados_finales()
    
    # Limpiar la sesión del usuario
    limpiar_sesion_usuario()

    return render_template("resultado_final.html", resultados=resultados)

@app.route("/peliculas", methods=["GET"])
def peliculas():
    """Página que muestra todas las películas ordenadas"""
    peliculas_index = trivia_game.obtener_peliculas_indexeada()
    return render_template('peliculas.html', peliculas=peliculas_index)

@app.route("/resultados", methods=["GET"])
def resultados():
    """Ruta que muestra los resultados históricos y los gráficos."""
    historicos = game_history.obtener_todos_juegos()
    graficos_procesador = GraficosProcesadorData(game_history)

    # Preparar los datos para todos los gráficos
    grafico_barras = graficos_procesador.get_performance_data()
    grafico_dispersion = graficos_procesador.get_efficiency_data()

    
    return render_template(
        'resultados_historicos.html',
        historicos=historicos,
        grafico_barras=grafico_barras,
        grafico_dispersion=grafico_dispersion,
        grafico_lineas=grafico_lineas(graficos_procesador),
        grafico_circular=grafico_circular(graficos_procesador)
    )

# Agregar la ruta para descargar el PDF
@app.route('/descargar_pdf')
def descargar_pdf():
    graficos_procesador = GraficosProcesadorData(game_history)
    return generar_pdf(graficos_procesador)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)