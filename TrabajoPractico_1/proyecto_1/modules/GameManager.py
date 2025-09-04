# modules/GameManager.py

from time import time
from modules.TriviaGame import TriviaGame
from datetime import datetime

class GameManager:
    def __init__(self):
        # Composition: The GameManager "has-a" TriviaGame object
        self.trivia_data = TriviaGame()
        
        # Variables de instancia (antes eran de sesión)
        self.usuario = None
        self.num_frases = 0
        self.aciertos = 0
        self.preguntas_hechas = []
        self.pregunta_actual = None
        self.tiempo_inicio = ""
        self.tiempo_inicioSeg = 0
    
    def obtener_usuario(self):
        return self.usuario

    def iniciar_juego(self, nombre_usuario, num_frases):
        """Inicializa los datos para un nuevo juego."""
        self.usuario = nombre_usuario
        self.num_frases = int(num_frases)
        self.aciertos = 0
        self.preguntas_hechas = []
        self.pregunta_actual = None
        self.tiempo_inicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tiempo_inicioSeg = time()

    def obtener_pregunta_nueva(self):
        """
        Devuelve una nueva pregunta que no ha sido usada en el juego actual.
        """
        # Obtener una nueva pregunta de la clase TriviaGame
        while True:
            pregunta = self.trivia_data.obtener_opciones()
            if pregunta['frase'] not in self.preguntas_hechas:
                break

        # Almacenar la pregunta actual y actualizar la lista de preguntas realizadas
        self.pregunta_actual = pregunta
        self.preguntas_hechas.append(pregunta['frase'])
        
        return pregunta

    def verificar_respuesta_y_actualizar_sesion(self, respuesta_usuario):
        """
        Verifica la respuesta del usuario y actualiza el puntaje.
        Devuelve una tupla (mensaje, categoria).
        """
        if not self.pregunta_actual:
            return ("No hay una pregunta activa.", "error")

        es_correcta = self.trivia_data.verificar_respuesta(self.pregunta_actual, respuesta_usuario)

        if es_correcta:
            self.aciertos += 1
            return ("¡Respuesta correcta! 🎉", "success")
        else:
            return (f"Respuesta incorrecta. La opción correcta era: {self.pregunta_actual['pelicula_correcta']} 😔", "error")

    def juego_terminado(self):
        """Verifica si el juego ha terminado."""
        return len(self.preguntas_hechas) >= self.num_frases


    def obtener_resultados_finales(self):

        porcentaje = (self.aciertos / self.num_frases * 100) if self.num_frases > 0 else 0
        duracion = time() - self.tiempo_inicioSeg

 
        resultados = {
            "usuario": self.usuario,
            "duracion": duracion,
            "tiempo_inicio": self.tiempo_inicio,
            "aciertos": self.aciertos,
            "num_frases": self.num_frases,
            "porcentaje": porcentaje
        }
        return resultados

    def obtener_resultado_final_dict(self):
        """Devuelve los resultados finales del juego como un diccionario."""
        resultados = self.obtener_resultados_finales()
        return {
            "usuario": resultados["usuario"],
            "aciertos": resultados["aciertos"],
            "num_frases": resultados["num_frases"],
            "porcentaje": resultados["porcentaje"],
            "tiempo_inicio": resultados["tiempo_inicio"],
            "duracion": resultados["duracion"]
        }

    def clear(self):
        """Limpia todas las variables para el próximo juego."""
        self.usuario = None
        self.num_frases = 0
        self.aciertos = 0
        self.preguntas_hechas = []
        self.pregunta_actual = None
        self.tiempo_inicio = ""
        self.tiempo_inicioSeg = 0