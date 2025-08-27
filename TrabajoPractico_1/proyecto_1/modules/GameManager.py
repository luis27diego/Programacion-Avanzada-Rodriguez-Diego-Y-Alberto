# modules/GameManager.py

from flask import session
import random
from modules.TriviaGame import TriviaGame

class GameManager:
    def __init__(self):
        # Composition: The GameManager "has-a" TriviaGame object
        self.trivia_data = TriviaGame()

    def iniciar_juego(self, nombre_usuario, num_frases):
        """Inicializa los datos de la sesión para un nuevo juego."""
        session['usuario'] = nombre_usuario
        session['num_frases'] = int(num_frases)
        session['aciertos'] = 0
        session['preguntas_hechas'] = []
        session.modified = True

    def obtener_pregunta_nueva(self):
        """
        Devuelve una nueva pregunta que no ha sido usada en la sesión actual.
        """
        preguntas_hechas = session.get('preguntas_hechas', [])
        
        # Get a new question from the TriviaGame class
        while True:
            pregunta = self.trivia_data.obtener_opciones()
            if pregunta['frase'] not in preguntas_hechas:
                break
        
        # Store the current question and update the list of asked questions
        session['pregunta_actual'] = pregunta
        preguntas_hechas.append(pregunta['frase'])
        session['preguntas_hechas'] = preguntas_hechas
        session.modified = True
        
        return pregunta

    def verificar_respuesta_y_actualizar_sesion(self, respuesta_usuario):
        """
        Verifica la respuesta del usuario y actualiza el puntaje en la sesión.
        Devuelve una tupla (mensaje, categoria).
        """
        pregunta_actual = session.get('pregunta_actual')
        if not pregunta_actual:
            return ("No hay una pregunta activa.", "error")

        es_correcta = self.trivia_data.verificar_respuesta(pregunta_actual, respuesta_usuario)

        if es_correcta:
            session['aciertos'] = session.get('aciertos', 0) + 1
            session.modified = True
            return ("¡Respuesta correcta! 🎉", "success")
        else:
            return (f"Respuesta incorrecta. La opción correcta era: {pregunta_actual['pelicula_correcta']} 😔", "error")

    def juego_terminado(self):
        """Verifica si el juego ha terminado."""
        
        return len(session.get('preguntas_hechas', [])) >= session.get('num_frases', 0)

    def obtener_resultados_finales(self):
        """Devuelve los datos finales del juego y limpia la sesión."""
        usuario = session.get('usuario')
        aciertos = session.get('aciertos')
        total = session.get('num_frases')
        porcentaje = (aciertos / total * 100) if total > 0 else 0

        session.clear()
        return usuario, aciertos, total, porcentaje


