# Ejemplo de aplicación principal en Flask
from flask import render_template, request,redirect, url_for, flash, session
from modules.config import app
from modules.validaciones import validar_parametros
from modules.TriviaGame import TriviaGame
from modules.GameManager import GameManager
from modules.GameHistoria import HistorialJuego
#from modules.RegistroSesiones import RegistroSesiones

#Registros = RegistroSesiones()
app.secret_key = 'una_clave_secreta_muy_larga_y_unica'
  
#Instancia la clase TriviaGame 
trivia_game = TriviaGame()
# Instanciamos la clase GameManager para la lógica del juego
game_manager = GameManager()
# Instanciamos la clase HistorialJuego para el registro de sesiones
game_history = HistorialJuego()

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
    
    # Inicia el juego usando el GameManager
    game_manager.iniciar_juego(data['nombre'], data['n'])
    return redirect(url_for("jugar_pregunta"))

@app.route("/jugar_pregunta", methods=["GET", "POST"])
def jugar_pregunta():
    """Ruta para cada pregunta del juego."""
    # Verificamos si hay una sesión de juego activa
    if 'usuario' not in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        respuesta_usuario = request.form.get('opcion')
        mensaje, categoria = game_manager.verificar_respuesta_y_actualizar_sesion(respuesta_usuario)
        flash(mensaje, categoria)

        # Si el juego ha terminado después de esta respuesta, redirige a la página de resultados finales.
        if game_manager.juego_terminado():
            sessionterminada = game_manager.obtener_resultados_finales()
            game_history.agregar_juego(sessionterminada)
            return redirect(url_for("mostrar_resultado_final", mensaje=mensaje, categoria=categoria))
        else:
            # Si el juego no ha terminado, redirige para la próxima pregunta.
            return redirect(url_for("jugar_pregunta"))
    
    else:
        # Lógica para mostrar la siguiente pregunta.
        pregunta = game_manager.obtener_pregunta_nueva()
        return render_template("jugar_pregunta.html", pregunta=pregunta)

@app.route("/mostrar_resultado_final")
def mostrar_resultado_final():
    if 'usuario' not in session:
        return redirect(url_for("home"))
    
    # Obtener los parámetros de la URL
    mensaje = request.args.get("mensaje")
    categoria = request.args.get("categoria")

    usuario, aciertos, total, porcentaje, tiempo_inicio, duracion = game_manager.obtener_resultados_finales(1)
    return render_template(
        "resultado_final.html",
        usuario=usuario,
        aciertos=aciertos,
        total=total,
        porcentaje=porcentaje,
        ultimo_mensaje=mensaje,
        ultima_categoria=categoria,
        tiempo_inicio=tiempo_inicio,
        duracion=duracion
    )
    
@app.route("/peliculas", methods=["GET"])
def peliculas():
    """
    Página que muestra todas las películas ordenadas
    """

    peliculas_index = trivia_game.obtener_peliculas_indexeada()
    return render_template('peliculas.html', peliculas=peliculas_index)

@app.route("/resultados", methods=["GET"])
def resultados():
    #Registros.agregar_sesion(session)
    return render_template("resultados.html", usuario=session['usuario'], aciertos=session['aciertos'], total=session['num_frases'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)