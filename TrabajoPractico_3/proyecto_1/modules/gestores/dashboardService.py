from modules.repositoriosABC.repositorioABC import RepositorioAbstracto
from modules.utilidades.monticulos.monticulobinario import MonticuloMedianaBinario
from datetime import datetime
from collections import Counter
from typing import List, Tuple
import spacy

nlp = spacy.load("es_core_news_sm")

class DashboardService:
    def __init__(self, usuario_repo: RepositorioAbstracto, reclamo_repo: RepositorioAbstracto):
        self.__usuario_repo = usuario_repo
        self.__reclamo_repo = reclamo_repo
        self.__stopwords = nlp.Defaults.stop_words  # Stopwords de spaCy
        
    def obtener_analiticas(self, id_departamento: int, id_usuario: int) -> dict:
        # Verifica el rol del usuario (por ejemplo, jefe o secretario) usando usuario_repo
        usuario = self.__usuario_repo.obtener_registro_por_filtro('id',id_usuario)
        if usuario.rol in ['SECRETARIO_TECNICO']:
            reclamos = self.__reclamo_repo.obtener_todos_los_registros()
            total = len(reclamos)
        else:
            #usuarios jefes solo ven los de su departamento
            reclamos = self.__reclamo_repo.obtener_registros_por_filtro('departamento_id',id_departamento)
            total = len(reclamos)

        # Calcula estadísticas (lógica de negocio aquí)
        # Datos para el gráfico de torta
        conteo_estados = self.__contar_estados(reclamos)
        datos_torta = {
            estado: (cantidad / total * 100) if total > 0 else 0
            for estado, cantidad in conteo_estados.items()
        }
        # mediana de tiempo en proceso
        mediana_en_proceso = self.__mediana_proceso(reclamos)

        # Mediana de tiempo resolución (si aplica)
        mediana_resolucion = self.__mediana_resolucion(reclamos)

        # Mediana de tiempo pendiente (si aplica)
        mediana_pendiente = self.__mediana_pendiente(reclamos)
  
        # Datos Nubes de palabras 
        contenidos_reclamos = [reclamo.contenido for reclamo in reclamos]
        datos_nube_palabras = self.__preparar_datos_nube_palabras(contenidos_reclamos)

        return {
            'datos_torta': datos_torta,
            'mediana_en_proceso': mediana_en_proceso,
            'mediana_resolucion': mediana_resolucion,
            'mediana_pendiente': mediana_pendiente,
            'datos_nube_palabras': datos_nube_palabras
        }
    
    def __contar_estados(self, reclamos) -> dict:
        conteo = {}
        for reclamo in reclamos:
            estado = reclamo.estado.value if hasattr(reclamo.estado, 'value') else reclamo.estado
            if estado not in conteo:
                conteo[estado] = 0
            conteo[estado] += 1
        return conteo
    
    def __mediana_pendiente(self,reclamos) -> list:
        tiempos = MonticuloMedianaBinario()
        for reclamo in reclamos:
            if reclamo.estado.value == 'pendiente':
                dias_pendiente = int((datetime.now() - reclamo.timestamp).total_seconds())
                #print(dias_pendiente)
                tiempos.insertar(dias_pendiente)
        return tiempos.valor_mediana
    
    def __mediana_proceso(self,reclamos) -> list:
        tiempos = MonticuloMedianaBinario()
        for reclamo in reclamos:
            if reclamo.estado.value == 'en_proceso' and reclamo.timestamp_modificacion:
                dias_en_proceso = int((datetime.now() - reclamo.timestamp_modificacion).total_seconds())
                #print(dias_en_proceso)
                tiempos.insertar(dias_en_proceso)
        return tiempos.valor_mediana
    
    def __mediana_resolucion(self,reclamos) -> list:
        tiempos = MonticuloMedianaBinario()
        for reclamo in reclamos:
            if reclamo.estado.value == 'resuelto' and reclamo.timestamp_modificacion:
                dias_resolucion = int((reclamo.timestamp_modificacion - reclamo.timestamp).total_seconds())
                #print(dias_resolucion)
                tiempos.insertar(dias_resolucion)
        return tiempos.valor_mediana

    def __preparar_datos_nube_palabras(self, contenidos_reclamos: List[str], top_n: int = 15) -> List[Tuple[str, int]]:
        # Unir todos los contenidos y convertir a minúsculas
        texto_total = ' '.join(contenidos_reclamos).lower()

        # Tokenizar con spaCy
        doc = nlp(texto_total)

        # Filtrar palabras vacías y signos de puntuación, y limpiar caracteres problemáticos
        palabras = [token.text.strip() for token in doc if token.text not in self.__stopwords and not token.is_punct]
        
        # Eliminar cualquier palabra que contenga saltos de línea u otros caracteres problemáticos
        palabras = [palabra.replace('\n', '').replace('\r', '') for palabra in palabras]

        # Contar frecuencias de palabras
        conteo_palabras = Counter(palabras)

        # Devolver las top_n palabras más comunes
        return conteo_palabras.most_common(top_n)
    

if __name__ == "__main__":    
    from modules.factoria import crear_repositorio
    usuario_repo, reclamo_repo, departamento_repo = crear_repositorio()
    dashboard_service = DashboardService(usuario_repo, reclamo_repo)
    analiticas = dashboard_service.obtener_analiticas(id_departamento=1, id_usuario=1)
    print(analiticas)
    


