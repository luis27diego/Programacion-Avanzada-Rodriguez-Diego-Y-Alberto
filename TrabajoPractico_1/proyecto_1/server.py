# Ejemplo de aplicación principal en Flask
from flask import render_template, request,redirect, url_for, flash, session
from modules.config import app
from modules.validaciones import validar_parametros
from modules.TriviaGame import TriviaGame
from modules.GameManager import GameManager
from modules.RegistroSesiones import RegistroSesiones

Registros = RegistroSesiones()
app.secret_key = 'una_clave_secreta_muy_larga_y_unica'
trivia_game = TriviaGame()
# Instanciamos la clase GameManager para la lógica del juego
game_manager = GameManager()

# Página de inicio
@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("inicio.html")

""" @app.route("/jugar", methods=["POST"])
def jugar():
    ok, data = validar_parametros(
        request.form.get("nombre"),
        request.form.get("num_frases")
    )
    if not ok:
        flash(data)
        return redirect(url_for("home"))

    # Por ahora solo mostramos un placeholder; más adelante implementamos la trivia real
    return f"TODO: iniciar trivia para {data['nombre']} con {data['n']} frases.(en construcción)" """

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

    # Si el juego ha terminado, redirige a la página de resultados
    if game_manager.juego_terminado():
        return redirect(url_for("mostrar_resultado_final"))
    
    if request.method == "POST":
        # Maneja la respuesta del usuario
        respuesta_usuario = request.form.get('opcion')
        mensaje, categoria = game_manager.verificar_respuesta_y_actualizar_sesion(respuesta_usuario)
        flash(mensaje, categoria)
        return redirect(url_for("jugar_pregunta"))

    else:
        # Obtiene una nueva pregunta y la muestra
        pregunta = game_manager.obtener_pregunta_nueva()
        return render_template("jugar_pregunta.html", pregunta=pregunta)
    
@app.route("/peliculas", methods=["GET"])
def peliculas():
    """
    Página que muestra todas las películas ordenadas
    """

    peliculas_index = trivia_game.obtener_peliculas_indexeada()
    return render_template('peliculas.html', peliculas=peliculas_index)

@app.route("/resultados", methods=["GET"])
def resultados():
    Registros.agregar_sesion(session)
    return render_template("resultados.html", usuario=session['usuario'], aciertos=session['aciertos'], total=session['num_frases'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)