from collections import defaultdict
class Cajon:
    """Contenedor iterable para alimentos"""
    
    def __init__(self, capacidad_maxima):
        self._capacidad_maxima = capacidad_maxima
        self._alimentos = []
        self._indice_iteracion = 0
    
    @property
    def capacidad_maxima(self):
        return self._capacidad_maxima
    
    @property
    def cantidad_actual(self):
        return len(self._alimentos)
    
    def agregar_alimento(self, alimento):
        """Agrega un alimento al cajón si hay espacio"""
        if self.esta_lleno():
            raise ValueError(f"Cajón lleno. Capacidad máxima: {self._capacidad_maxima}")
        
        if not hasattr(alimento, 'calcular_aw'):
            raise TypeError("El objeto debe ser un alimento válido")
        
        self._alimentos.append(alimento)
    
    def esta_lleno(self):
        """Verifica si el cajón está lleno"""
        return len(self._alimentos) >= self._capacidad_maxima
    
    def peso_total(self):
        """Calcula el peso total del cajón"""
        return sum(alimento.peso for alimento in self._alimentos)
    def aw_promedio_total(self):
        """Calcula la actividad acuosa promedio total del cajón"""
        if not self._alimentos:
            return 0.0
        
        total_aw = sum(alimento.calcular_aw() for alimento in self._alimentos)
        return total_aw / len(self._alimentos)
    
    def aw_promedio_por_alimento(self):
        """Calcula el promedio de aw por cada tipo de alimento"""
        if not self._alimentos:
            return {}
        
        # Agrupa alimentos por nombre
        grupos = defaultdict(list)
        for alimento in self._alimentos:
            grupos[alimento.nombre].append(alimento.calcular_aw())
        
        # Calcula promedio para cada grupo
        promedios = {}
        for nombre, aw_values in grupos.items():
            promedios[f"aw_prom_{nombre.lower()}"] = sum(aw_values) / len(aw_values)
        
        return promedios
    
    def aw_promedio_por_tipo(self):
        """Calcula el promedio de aw por tipo (frutas/verduras)"""
        if not self._alimentos:
            return {"aw_prom_frutas": 0.0, "aw_prom_verduras": 0.0}
        
        from .Alimentos import Fruta, Verdura  # Import local para evitar circular
        
        frutas = [alimento for alimento in self._alimentos if isinstance(alimento, Fruta)]
        verduras = [alimento for alimento in self._alimentos if isinstance(alimento, Verdura)]
        
        resultado = {}
        
        if frutas:
            total_aw_frutas = sum(alimento.calcular_aw() for alimento in frutas)
            resultado["aw_prom_frutas"] = total_aw_frutas / len(frutas)
        else:
            resultado["aw_prom_frutas"] = 0.0
        
        if verduras:
            total_aw_verduras = sum(alimento.calcular_aw() for alimento in verduras)
            resultado["aw_prom_verduras"] = total_aw_verduras / len(verduras)
        else:
            resultado["aw_prom_verduras"] = 0.0
        
        return resultado
    
    def obtener_advertencias(self):
        """Obtiene lista de advertencias para valores de aw > 0.90"""
        advertencias = []
        
        # Verificar promedio total
        aw_total = self.aw_promedio_total()
        if aw_total > 0.90:
            advertencias.append(f"⚠️ Actividad acuosa total elevada: {aw_total:.3f}")
        
        # Verificar promedios por alimento
        promedios_alimento = self.aw_promedio_por_alimento()
        for nombre, valor in promedios_alimento.items():
            if valor > 0.90:
                advertencias.append(f"⚠️ {nombre}: {valor:.3f}")
        
        # Verificar promedios por tipo
        promedios_tipo = self.aw_promedio_por_tipo()
        if promedios_tipo["aw_prom_frutas"] > 0.90:
            advertencias.append(f"⚠️ Promedio frutas elevado: {promedios_tipo['aw_prom_frutas']:.3f}")
        if promedios_tipo["aw_prom_verduras"] > 0.90:
            advertencias.append(f"⚠️ Promedio verduras elevado: {promedios_tipo['aw_prom_verduras']:.3f}")
        
        return advertencias
    
    # Implementación del protocolo de iteración
    def __iter__(self):
        """Hace el cajón iterable"""
        self._indice_iteracion = 0
        return self

    def __next__(self):
        """Retorna el siguiente alimento en la iteración"""
        if self._indice_iteracion >= len(self._alimentos):
            raise StopIteration
        
        alimento = self._alimentos[self._indice_iteracion]
        self._indice_iteracion += 1
        return alimento

if __name__ == "__main__":
    from Frutas import Kiwi, Manzana
    from Verduras import Papa, Zanahoria
    
    # Crear un cajón
    cajon = Cajon(5)
    
    # Agregar alimentos
    try:
        cajon.agregar_alimento(Kiwi(150))
        cajon.agregar_alimento(Manzana(200))
        cajon.agregar_alimento(Papa(300))
        cajon.agregar_alimento(Zanahoria(100))
        cajon.agregar_alimento(Manzana(180))
        
        print("=== ITERACIÓN DEL CAJÓN ===")
        for alimento in cajon:
            print(f"  {alimento}")
        
        print(f"\n{cajon}")
        print(f"\n{cajon.obtener_advertencias()}")
        
    except Exception as e:
        print(f"Error: {e}")