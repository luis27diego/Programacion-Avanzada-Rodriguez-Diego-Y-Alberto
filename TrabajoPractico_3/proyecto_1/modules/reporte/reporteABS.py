from abc import ABC, abstractmethod

class ReporteABS(ABC):
    @abstractmethod
    def generar_reporte(self, datos: dict, graficos: dict):
        pass
