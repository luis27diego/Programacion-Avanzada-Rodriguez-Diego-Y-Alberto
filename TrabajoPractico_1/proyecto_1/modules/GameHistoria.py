import json
import os

class HistorialJuego:
    def __init__(self, archivo_historial: str = "data/historial_juego.json"):
        self.archivo_historial = archivo_historial
        self.historial = []
        self.cargar_historial()
    
    def cargar_historial(self):
        """Carga el historial de juegos desde el archivo"""
        try:
            if os.path.exists(self.archivo_historial):
                with open(self.archivo_historial, 'r',   encoding='utf-8') as archivo:
                    self.historial = json.load(archivo)
            else:
                self.historial = []
        except (json.JSONDecodeError, FileNotFoundError):
            self.historial = []
    
    def guardar_historial(self):
        """Guarda el historial de juegos en el archivo"""
        try:
            os.makedirs(os.path.dirname(self.archivo_historial), exist_ok=True)
            with open(self.archivo_historial, 'w', encoding='utf-8') as archivo:
                json.dump(self.historial, archivo, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def agregar_juego(self, sesion):
        """Agrega una nueva sesión al historial"""
        registro_juego = {
            'usuario': sesion['usuario'],
            'aciertos': sesion['aciertos'],
            'tiempo_inicio': sesion['tiempo_inicio'],
            'num_frases': sesion['num_frases'],
            'duracion': sesion['duracion'],
            'porcentaje': sesion['porcentaje']
        }
        self.historial.append(registro_juego)
        self.guardar_historial()

    def obtener_todos_juegos(self):
        """Retorna todo el historial de juegos"""
        return self.historial
