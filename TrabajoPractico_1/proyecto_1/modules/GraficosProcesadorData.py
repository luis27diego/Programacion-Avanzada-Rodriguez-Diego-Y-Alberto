import datetime
class GraficosProcesadorData:
    def __init__(self, game_historia: list):    
        # game_historia es una lista de diccionarios con los datos de cada juego
        self.history_data = game_historia

    def obtener_datos_rendimiento(self):
        """
        Prepara los datos para el Gráfico 1 (Comparación de Rendimiento).
        Calcula el porcentaje de aciertos promedio para cada usuario.
        """
        user_scores = {}
        
        for game in self.history_data:
            usuario = game['usuario']
            porcentaje = game['porcentaje']

            if usuario not in user_scores:
                user_scores[usuario] = {'total_porcentaje': 0, 'juegos': 0}
            
            user_scores[usuario]['total_porcentaje'] += porcentaje
            user_scores[usuario]['juegos'] += 1

        labels = []
        data = []
        for usuario, scores in user_scores.items():
            promedio = scores['total_porcentaje'] / scores['juegos']
            labels.append(usuario)
            data.append(round(promedio, 2))
            
        return {'labels': labels, 'data': data}

    def obtener_datos_eficiencia(self):
        """
        Prepara los datos para el Gráfico 2 (Análisis de Eficiencia).
        Crea una lista de puntos con duración y porcentaje para cada partida.
        """
        x_data = [] # Eje X: duración
        y_data = [] # Eje Y: porcentaje de aciertos
        labels = [] # Nombres de los usuarios
        
        for game in self.history_data:
            duracion = game['duracion']
            porcentaje = game['porcentaje']

            x_data.append(duracion)
            y_data.append(round(porcentaje, 2))
            labels.append(game['usuario'])

        return {'x': x_data, 'y': y_data, 'labels': labels}
    
    def obtener_datos_lineas(self):
        """
        Prepara los datos para el Gráfico de Líneas (aciertos y desaciertos en el tiempo).
        """
        # Ordenamos los datos por fecha para el gráfico de líneas
        sorted_data = sorted(
            [x for x in self.history_data if x.get('tiempo_inicio')],
            key=lambda x: datetime.datetime.strptime(x['tiempo_inicio'], '%Y-%m-%d %H:%M:%S')
        )
        
        dates = []
        aciertos_data = []
        desaciertos_data = []
        
        for game in sorted_data:
            # Para el gráfico, usamos la fecha y hora de la partida
            dates.append(game['tiempo_inicio']) 
            aciertos_data.append(game['aciertos'])
            desaciertos_data.append(game['num_frases'] - game['aciertos'])
            
        return {
            'labels': dates,
            'datasets': [
                {
                    'label': 'Aciertos',
                    'data': aciertos_data,
                    'borderColor': 'rgba(34, 197, 94, 1)', # Verde
                    'backgroundColor': 'rgba(34, 197, 94, 0.2)',
                },
                {
                    'label': 'Desaciertos',
                    'data': desaciertos_data,
                    'borderColor': 'rgba(239, 68, 68, 1)', # Rojo
                    'backgroundColor': 'rgba(239, 68, 68, 0.2)',
                }
            ]
        }

    def obtener_datos_circular(self):
        """
        Prepara los datos para el Gráfico Circular (proporción total de aciertos vs. desaciertos).
        """
        total_aciertos = sum(game['aciertos'] for game in self.history_data)
        total_preguntas = sum(game['num_frases'] for game in self.history_data)
        total_desaciertos = total_preguntas - total_aciertos
        
        return {
            'labels': ['Aciertos', 'Desaciertos'],
            'data': [total_aciertos, total_desaciertos],
            'backgroundColor': ['rgba(34, 197, 94, 0.8)', 'rgba(239, 68, 68, 0.8)']
        }