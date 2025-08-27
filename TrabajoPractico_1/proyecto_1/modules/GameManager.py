# modules/GameManager.py

from time import time
from flask import session
import random
from modules.TriviaGame import TriviaGame
from datetime import datetime

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
        session['tiempo_inicio'] = datetime.now().strftime('%H:%M:%S')
        session['tiempo_inicioSeg'] = time()

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

    def obtener_resultados_finales(self,flag = None):

        if flag==1:
            """Devuelve los datos finales del juego sin limpiar la sesión."""
            usuario = session.get('usuario')
            aciertos = session.get('aciertos')
            total = session.get('num_frases')
            porcentaje = (aciertos / total * 100) if total > 0 else 0
            tiempo_inicio = session.get('tiempo_inicioSeg')
            tiempo_inicio_hr = session.get('tiempo_inicio')
            tiempo_final = time()
            duracion = tiempo_final - tiempo_inicio

            session.clear()
            return usuario, aciertos, total, porcentaje, tiempo_inicio_hr, duracion
        else:
            return {"usuario": session.get('usuario'), "duracion": (time() - session.get('tiempo_inicioSeg') ), "tiempo_inicio": session.get('tiempo_inicio'), "aciertos": session.get('aciertos'), "num_frases": session.get('num_frases'), "porcentaje": (session.get('aciertos') / session.get('num_frases') * 100) if session.get('num_frases') > 0 else 0}

    def obtener_resultado_final_dict(self):
        """Devuelve los resultados finales del juego como un diccionario."""
        usuario, aciertos, total, porcentaje, tiempo_inicio_hr, duracion = self.obtener_resultados_finales()
        return {
            "usuario": usuario,
            "aciertos": aciertos,
            "num_frases": total,
            "porcentaje": porcentaje,
            "tiempo_inicio": tiempo_inicio_hr,
            "duracion": duracion
        }
