# utilidades/graficos.py
from typing import Dict, List, Tuple
from wordcloud import WordCloud

import matplotlib
matplotlib.use('Agg')  # <-- Agrega esta línea antes de importar pyplot
from matplotlib import pyplot as plt
    
colores = [
    "#3B82F6",  # Azul
    "#0EA5E9",  # Azul claro
    "#F59E0B",  # Amarillo

]
def crear_figura_nube_palabras(datos_palabras: List[Tuple[str, int]]):
    """Crea y devuelve una figura de matplotlib con nube de palabras."""
    diccionario_palabras = dict(datos_palabras)
   
    wc = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='Blues',
        relative_scaling=0.5,
        min_font_size=10
    ).generate_from_frequencies(diccionario_palabras)
   
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Palabras Más Frecuentes en Reclamos', fontsize=18, pad=20)
    
    return fig

def crear_grafico_torta(datos_torta: Dict[str, float]) -> str:
    """Genera un gráfico de torta con un diseño inspirado en Plotly (colores, tipografía, fondo transparente)."""
    if not datos_torta:
        return "No hay datos para mostrar."

    etiquetas = list(datos_torta.keys())
    valores = list(datos_torta.values())

    # --- Limpieza de gráfico anterior ---
    plt.clf()

    # --- Creación del gráfico ---
    wedges, texts, autotexts = plt.pie(
        valores,
        labels=etiquetas,
        autopct='%1.1f%%',
        startangle=90,
        colors=colores[:len(valores)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )

    # --- Estilo del texto y fondo ---
    plt.setp(autotexts, size=12, weight='bold', color='white')
    plt.setp(texts, size=12)
    plt.title(
        "Porcentajes de Reclamos por Estado",
        fontsize=18,
        pad=20
    )

    plt.axis('equal')  # Mantiene forma circular
    plt.gcf().patch.set_alpha(0)  # Fondo transparente

    # --- Guardar imagen ---
    ruta = "static/grafico_torta.png"
    plt.savefig(ruta, bbox_inches='tight', dpi=200, transparent=True)
    plt.close()

    return ruta

def crear_barra_mediana(mediana_en_proceso: float, mediana_resueltos: float, mediana_pendiente: float) -> str:
    """Genera un gráfico de barras con estilo tipo Plotly."""
    categorias = ['Mediana En Proceso', 'Mediana Resueltos', 'Mediana Pendientes']
    valores = [mediana_en_proceso, mediana_resueltos, mediana_pendiente]

    plt.clf()

    # --- Crear gráfico de barras ---
    plt.bar(categorias, valores, color=colores, edgecolor='white', linewidth=1)

    # --- Estética general ---
    plt.title("Mediana de Tiempos de Resolución (días)", fontsize=18, pad=20)
    plt.ylabel("Días", fontsize=14)
    plt.xticks(fontsize=12, rotation=15)
    plt.yticks(fontsize=12)

    # Fondo transparente y márgenes similares al layout Plotly
    plt.gca().set_facecolor('none')  # Fondo del gráfico transparente
    plt.gcf().patch.set_alpha(0)     # Fondo del lienzo transparente
    plt.tight_layout(pad=2.0)

    # --- Guardar imagen ---
    ruta = "static/grafico_barra_mediana.png"
    plt.savefig(ruta, bbox_inches='tight', dpi=200, transparent=True)
    plt.close()

    return ruta

def crear_imagen_nube_palabras(datos_palabras: List[Tuple[str, int]]) -> str:
    """Crea nube de palabras, la guarda como archivo y devuelve HTML con tag <img>."""
    fig = crear_figura_nube_palabras(datos_palabras)
    
    # Guarda la imagen en un archivo
    
    ruta_imagen = 'static/nube_palabras.png'
    fig.savefig(ruta_imagen, bbox_inches='tight', dpi=200, facecolor='white')
    plt.close(fig)
    
    # Devuelve una etiqueta HTML para mostrar la imagen
    return ruta_imagen

# Prueba simple de las funciones
if __name__ == "__main__":
    datos_torta = {'Pendiente': 40, 'En Proceso': 35, 'Resueltos': 25}
    crear_grafico_torta(datos_torta)
    crear_barra_mediana(5, 10, 15)
 