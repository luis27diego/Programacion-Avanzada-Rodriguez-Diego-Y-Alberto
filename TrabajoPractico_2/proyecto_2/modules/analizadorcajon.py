from collections import defaultdict
from modules.Alimentos import Fruta, Verdura

class AnalizadorCajon:
    """Analiza un cajón y calcula estadísticas, promedios y advertencias."""
    
    def __init__(self, cajon):
        self.cajon = cajon
    
    # -------------------------
    # MÉTRICAS PRINCIPALES
    # -------------------------
    
    def peso_total(self):
        return sum(alimento.peso for alimento in self.cajon)
    
    def aw_promedio_total(self):
        alimentos = list(self.cajon)
        if not alimentos:
            return 0.0
        total_aw = sum(a.calcular_aw() for a in alimentos)
        return total_aw / len(alimentos)
    
    def aw_promedio_por_alimento(self):
        alimentos = list(self.cajon)
        if not alimentos:
            return {}
        
        grupos = defaultdict(list)
        for alimento in alimentos:
            grupos[alimento.nombre].append(alimento.calcular_aw())
        
        promedios = {}
        for nombre, valores in grupos.items():
            promedios[f"aw_{nombre.lower()}"] = sum(valores) / len(valores)
        return promedios
    
    def aw_promedio_por_tipo(self):
        alimentos = list(self.cajon)
        if not alimentos:
            return {"aw_prom_frutas": 0.0, "aw_prom_verduras": 0.0}
        
        frutas = [a for a in alimentos if isinstance(a, Fruta)]
        verduras = [a for a in alimentos if isinstance(a, Verdura)]
        
        resultado = {}
        resultado["aw_prom_frutas"] = (
            sum(a.calcular_aw() for a in frutas) / len(frutas)
            if frutas else 0.0
        )
        resultado["aw_prom_verduras"] = (
            sum(a.calcular_aw() for a in verduras) / len(verduras)
            if verduras else 0.0
        )
        return resultado

    # -------------------------
    # ADVERTENCIAS
    # -------------------------
    
    def generar_advertencias(self):
        advertencias = []
        
        aw_total = self.aw_promedio_total()
        if aw_total > 0.90:
            advertencias.append(f"⚠️ Actividad acuosa total elevada: {aw_total:.3f}")
        
        promedios_alimento = self.aw_promedio_por_alimento()
        for nombre, valor in promedios_alimento.items():
            if valor > 0.90:
                advertencias.append(f"⚠️ {nombre}: {valor:.3f}")
        
        promedios_tipo = self.aw_promedio_por_tipo()
        if promedios_tipo["aw_prom_frutas"] > 0.90:
            advertencias.append(f"⚠️ Promedio frutas elevado: {promedios_tipo['aw_prom_frutas']:.3f}")
        if promedios_tipo["aw_prom_verduras"] > 0.90:
            advertencias.append(f"⚠️ Promedio verduras elevado: {promedios_tipo['aw_prom_verduras']:.3f}")
        

        
        return advertencias
    
    def es_susceptible(self):
        """Determina si el cajón es susceptible a contaminación microbiana"""
        return self.aw_promedio_total() > 0.90
    

    # -------------------------
    # INFORME COMPLETO
    # -------------------------
    
    def generar_informe(self):
        """Devuelve un diccionario con todas las estadísticas y advertencias."""
        promedios_tipo = self.aw_promedio_por_tipo()
        promedios_alimento = self.aw_promedio_por_alimento()
        
        estadisticas = {
            "peso_total": self.peso_total(),
            "aw_total": self.aw_promedio_total(),
            "aw_frutas": promedios_tipo["aw_prom_frutas"],
            "aw_verduras": promedios_tipo["aw_prom_verduras"],
            **promedios_alimento
        }
        
        return {
            "estadisticas": estadisticas,
            "advertencias": self.generar_advertencias()
        }
