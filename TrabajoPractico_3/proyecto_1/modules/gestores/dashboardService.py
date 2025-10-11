from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from datetime import datetime
from statistics import median
from collections import Counter
from typing import List, Tuple

class DashboardService:
    def __init__(self, usuario_repo: RepositorioAbstracto, reclamo_repo: RepositorioAbstracto):
        self.usuario_repo = usuario_repo
        self.reclamo_repo = reclamo_repo

    def obtener_analiticas(self, id_departamento: int, id_usuario: int) -> dict:
        # Verifica el rol del usuario (por ejemplo, jefe o secretario) usando usuario_repo
        usuario = self.usuario_repo.obtener_registro_por_filtro('id',id_usuario)
        #if not self._has_access_to_dept(usuario, id_departamento):
        #    raise PermissionError("Acceso denegado")

        # Obtiene datos de reclamos vía reclamo_repo
        reclamos = self.reclamo_repo.obtener_registros_por_filtro('departamento_id',id_departamento)
        total = len(reclamos)

        # Calcula estadísticas (lógica de negocio aquí)
        # Datos para el gráfico de torta
        conteo_estados = self.__contar_estados(reclamos)
        datos_torta = {
            estado: (cantidad / total * 100) if total > 0 else 0
            for estado, cantidad in conteo_estados.items()
        }
        # mediana de tiempo en proceso
        tiempos_en_proceso = self.__tiempos_proceso(reclamos)
        mediana_en_proceso = median(tiempos_en_proceso) if tiempos_en_proceso else 0 #Cambiar a la implementacion del monticulo Binario

        # Mediana de tiempo resolución (si aplica)
        tiempos_resolucion = self.__tiempos_resolucion(reclamos)
        mediana_resolucion = median(tiempos_resolucion) if tiempos_resolucion else 0

        # Mediana de tiempo pendiente (si aplica)
        tiempos_pendiente = self.__tiempo_pendiente(reclamos)
        mediana_pendiente = median(tiempos_pendiente) if tiempos_pendiente else 0

        # Datos Nubes de palabras 
        contenidos_reclamos = [reclamo.contenido for reclamo in reclamos]
        datos_nube_palabras = self.__preparar_datos_nube_palabras(contenidos_reclamos)

        return {
            'datos_torta': datos_torta,
            'mediana_en_proceso': mediana_en_proceso,
            'mediana_resolucion': mediana_resolucion,
            'mediana_pendiente': mediana_pendiente,
            'datos_nube_palabras': datos_nube_palabras
            # Otros datos...
        }
    
    def __contar_estados(self, reclamos) -> dict:
        conteo = {}
        for reclamo in reclamos:
            estado = reclamo.estado.value if hasattr(reclamo.estado, 'value') else reclamo.estado
            if estado not in conteo:
                conteo[estado] = 0
            conteo[estado] += 1
        return conteo
    
    def __tiempo_pendiente(self,reclamos) -> list:
        tiempos = []
        for reclamo in reclamos:
            if reclamo.estado.value == 'pendiente':
                dias_pendiente = int((datetime.now() - reclamo.timestamp).total_seconds())
                #print(dias_pendiente)
                tiempos.append(dias_pendiente)
        return tiempos
    
    def __tiempos_proceso(self,reclamos) -> list:
        tiempos = []
        for reclamo in reclamos:
            if reclamo.estado.value == 'en_proceso' and reclamo.timestamp_modificacion:
                dias_en_proceso = int((datetime.now() - reclamo.timestamp_modificacion).total_seconds())
                #print(dias_en_proceso)
                tiempos.append(dias_en_proceso)
        return tiempos
    
    def __tiempos_resolucion(self,reclamos) -> list:
        tiempos = []
        for reclamo in reclamos:
            if reclamo.estado.value == 'resuelto' and reclamo.timestamp_modificacion:
                dias_resolucion = int((reclamo.timestamp_modificacion - reclamo.timestamp).total_seconds())
                #print(dias_resolucion)
                tiempos.append(dias_resolucion)
        return tiempos

    def __preparar_datos_nube_palabras(self, contenidos_reclamos: List[str], top_n: int = 15) -> List[Tuple[str, int]]:
        # Lista básica de palabras vacías (puedes usar NLTK para una más completa)
        stopwords = {'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'un', 'una', 'por', 'con'}
        
        # Unir todos los contenidos y convertir a minúsculas
        texto_total = ' '.join(contenidos_reclamos).lower()
        
        # Tokenizar (separar en palabras) y filtrar palabras vacías
        palabras = [palabra.strip('.,!?') for palabra in texto_total.split() if palabra.strip('.,!?') not in stopwords]
        
        # Contar frecuencias
        conteo_palabras = Counter(palabras)
        
        # Devolver las top_n palabras más frecuentes
        return conteo_palabras.most_common(top_n)
    

if __name__ == "__main__":    
    from modules.factoria import crear_repositorio
    usuario_repo, reclamo_repo, departamento_repo = crear_repositorio()
    dashboard_service = DashboardService(usuario_repo, reclamo_repo)
    analiticas = dashboard_service.obtener_analiticas(id_departamento=1, id_usuario=1)
    print(analiticas)


