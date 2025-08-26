# Ejemplo de aplicación principal en Flask
from flask import render_template, request,redirect, url_for, flash
from modules.config import app
from modules.validaciones import validar_parametros
from modules.TriviaGame import TriviaGame

trivia_game = TriviaGame()

# Página de inicio
@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("inicio.html")

@app.route("/jugar", methods=["POST"])
def jugar():
    ok, data = validar_parametros(
        request.form.get("nombre"),
        request.form.get("num_frases")
    )
    if not ok:
        flash(data)
        return redirect(url_for("home"))

    # Por ahora solo mostramos un placeholder; más adelante implementamos la trivia real
    return f"TODO: iniciar trivia para {data['nombre']} con {data['n']} frases.(en construcción)"

@app.route("/peliculas", methods=["GET"])
def peliculas():
    """
    Página que muestra todas las películas ordenadas
    """

    peliculas_index = trivia_game.obtener_peliculas_indexeada()
    return render_template('peliculas.html', peliculas=peliculas_index)

@app.route("/resultados", methods=["GET"])
def resultados():
    return "TODO: resultados históricos (en construcción)."
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)