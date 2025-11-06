# utilidades/graficos.py
from typing import Dict, List, Tuple
from wordcloud import WordCloud

import matplotlib
matplotlib.use('Agg')  # <-- Agrega esta línea antes de importar pyplot
from matplotlib import pyplot as plt
    

def crear_figura_nube_palabras(datos_palabras: List[Tuple[str, int]]):
    """Crea y devuelve una figura de matplotlib con nube de palabras."""
    diccionario_palabras = dict(datos_palabras)
   
    wc = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        relative_scaling=0.5,
        min_font_size=10
    ).generate_from_frequencies(diccionario_palabras)
   
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Palabras Más Frecuentes en Reclamos', fontsize=18, pad=20)
    
    return fig

# ============================================================================

def crear_grafico_torta(datos_torta: Dict[str, float]) -> str:
    """Genera un gráfico de torta con un diseño inspirado en Plotly (colores, tipografía, fondo transparente)."""
    if not datos_torta:
        return "No hay datos para mostrar."

    etiquetas = list(datos_torta.keys())
    valores = list(datos_torta.values())

    # --- Estilo de colores similar al de Plotly ---
    colores = [
        "#636EFA",  # Azul
        "#EF553B",  # Rojo coral
        "#00CC96",  # Verde esmeralda
        "#AB63FA",  # Violeta
        "#FFA15A",  # Naranja
        "#19D3F3",  # Celeste
        "#FF6692",  # Rosa
        "#B6E880",  # Verde claro
        "#FF97FF",  # Fucsia
        "#FECB52",  # Amarillo
    ]

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
    categorias = ['Mediana Pendiente', 'Mediana En Proceso', 'Mediana Resueltos']
    valores = [mediana_pendiente, mediana_en_proceso, mediana_resueltos]

    # --- Colores estilo Plotly ---
    colores = ["#636EFA",  "#EF553B",  "#00CC96"]  
    plt.clf()

    # --- Crear gráfico de barras ---
    barras = plt.bar(categorias, valores, color=colores, edgecolor='white', linewidth=1)

    # --- Estética general ---
    plt.title("Mediana de Tiempos de Resolución (días)", fontsize=18, pad=20)
    plt.ylabel("Días", fontsize=14)
    plt.xticks(fontsize=12, rotation=15)
    plt.yticks(fontsize=12)

    # Fondo transparente y márgenes similares al layout Plotly
    plt.gca().set_facecolor('none')  # Fondo del gráfico transparente
    plt.gcf().patch.set_alpha(0)     # Fondo del lienzo transparente
    plt.tight_layout(pad=2.0)

    # --- Añadir valores encima de las barras ---
    for barra in barras:
        y = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            y + (max(valores) * 0.02),
            f"{y:.1f}",
            ha='center',
            va='bottom',
            fontsize=12,
            weight='bold'
        )

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
 