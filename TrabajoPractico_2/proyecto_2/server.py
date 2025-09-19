# app.py
from flask import Flask, render_template, request, redirect, url_for
import random
from modules.Frutas import Kiwi, Manzana
from modules.Verduras import Papa, Zanahoria
from modules.Cajon import Cajon

app = Flask(__name__)
app.secret_key = 'smart_belt_secret_key_2024'
def crear_alimento(tipo, peso):
    """Crea una instancia del alimento correspondiente según el tipo."""
    tipo = tipo.lower()
    if tipo == "kiwi":
        return Kiwi(peso)
    elif tipo == "manzana":
        return Manzana(peso)
    elif tipo == "papa":
        return Papa(peso)
    elif tipo == "zanahoria":
        return Zanahoria(peso)
    else:
        raise ValueError(f"Tipo de alimento no reconocido: {tipo}")

class CintaTransportadora:
    """Simula la cinta transportadora con detección de alimentos"""
    
    @staticmethod
    def detectar_alimento():
        """Simula la detección del alimento como lo haría la clase de la cátedra"""
        # Simula 10% de probabilidad de fallo en la detección
        if random.random() < 0.1:
            return "undefined"
        
        # Tipos de alimentos disponibles
        tipos = ['kiwi', 'manzana', 'papa', 'zanahoria']
        tipo = random.choice(tipos)
        peso = random.randint(50, 450)  # Peso entre 50-450g
        
        return {
            "alimento": tipo,
            "peso": peso
        }

class ControladorSistema:
    """Controlador principal del sistema Smart Belt"""
    
    def __init__(self):
        self.cinta = CintaTransportadora()
        self.cajon_actual = None
        self.estado = "idle"  # idle, running, complete
        self.alimentos_procesados = 0
        self.alimentos_desviados = 0
    
    def iniciar_proceso(self, capacidad_cajon):
        """Inicia el proceso de carga de un nuevo cajón"""
        self.cajon_actual = Cajon(capacidad_cajon)
        self.estado = "running"
        self.alimentos_procesados = 0
        self.alimentos_desviados = 0
        return True
    
    def procesar_siguiente_alimento(self):
        """Procesa el siguiente alimento de la cinta"""
        if self.estado != "running" or not self.cajon_actual:
            return False
        
        # Verificar si el cajón está lleno
        if self.cajon_actual.esta_lleno():
            self.estado = "complete"
            return False
        
        # Detectar alimento
        deteccion = self.cinta.detectar_alimento()
        
        if deteccion == "undefined":
            # Alimento desviado por falla en detección
            self.alimentos_desviados += 1
            return {"tipo": "desviado", "mensaje": "Alimento desviado por falla en detección"}
        
        try:
            # Crear y agregar alimento al cajón
            alimento = crear_alimento(deteccion["alimento"], deteccion["peso"])
            self.cajon_actual.agregar_alimento(alimento)
            self.alimentos_procesados += 1
            
            return {
                "tipo": "agregado",
                "alimento": deteccion["alimento"],
                "peso": deteccion["peso"],
                "aw": alimento.calcular_aw()
            }
            
        except Exception as e:
            # Error al crear o agregar alimento
            self.alimentos_desviados += 1
            return {"tipo": "error", "mensaje": str(e)}
    
    def obtener_estado_actual(self):
        """Retorna el estado actual completo del sistema"""
        if not self.cajon_actual:
            return {
                "estado": self.estado,
                "progreso": {"actual": 0, "total": 0},
                "estadisticas": {},
                "advertencias": []
            }
        
        # Calcular estadísticas
        estadisticas = {
            "peso_total": self.cajon_actual.peso_total() / 1000,  # Convertir a kg
            "aw_total": self.cajon_actual.aw_promedio_total(),
            "alimentos_procesados": self.alimentos_procesados,
            "alimentos_desviados": self.alimentos_desviados
        }
        
        # Promedios por tipo
        promedios_tipo = self.cajon_actual.aw_promedio_por_tipo()
        estadisticas["aw_frutas"] = promedios_tipo["aw_prom_frutas"]
        estadisticas["aw_verduras"] = promedios_tipo["aw_prom_verduras"]
        
        # Promedios por alimento
        promedios_alimento = self.cajon_actual.aw_promedio_por_alimento()
        estadisticas["aw_kiwi"] = promedios_alimento.get("aw_prom_kiwi", 0)
        estadisticas["aw_manzana"] = promedios_alimento.get("aw_prom_manzana", 0)
        estadisticas["aw_papa"] = promedios_alimento.get("aw_prom_papa", 0)
        estadisticas["aw_zanahoria"] = promedios_alimento.get("aw_prom_zanahoria", 0)
        
        return {
            "estado": self.estado,
            "progreso": {
                "actual": self.cajon_actual.cantidad_actual,
                "total": self.cajon_actual.capacidad_maxima
            },
            "estadisticas": estadisticas,
            "advertencias": self.cajon_actual.obtener_advertencias()
        }

# Instancia global del controlador
controlador = ControladorSistema()


# Nueva lógica: todo el flujo se maneja por rutas y recarga de página
@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = None
    error = None
    estado = controlador.obtener_estado_actual()
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