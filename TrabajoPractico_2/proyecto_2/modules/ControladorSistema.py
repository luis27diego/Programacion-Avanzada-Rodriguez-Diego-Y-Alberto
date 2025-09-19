
from modules.CintaTransportadora import DetectorAlimento
from modules.Cajon import Cajon
from modules.Crear_alimento import crear_alimento

class ControladorSistema:
    """Controlador principal del sistema Smart Belt"""
    
    def __init__(self):
        self.cinta = DetectorAlimento()
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
            print(deteccion["peso"])
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
            "peso_total": self.cajon_actual.peso_total(),  # Convertir a kg
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
