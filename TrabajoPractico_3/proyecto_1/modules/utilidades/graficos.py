# utilidades/graficos.py

import plotly.express as px
import plotly.io as pio
import numpy as np
from typing import Dict, List, Tuple
from wordcloud import WordCloud

import matplotlib
matplotlib.use('Agg')  # <-- Agrega esta línea antes de importar pyplot
from matplotlib import pyplot as plt
    

def crear_grafico_torta(datos_torta: Dict[str, float]) -> str:
    """Recibe un dict de estado -> porcentaje y devuelve HTML para Plotly.js."""
    if not datos_torta:
        return '<div>No hay datos para mostrar.</div>'
    
    fig = px.pie(
        values=list(datos_torta.values()),
        names=list(datos_torta.keys()),
        title='Porcentajes de Reclamos por Estado',
        hole=0.3
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        title_font_size=18,
        margin=dict(t=60, b=20, l=20, r=20)
    )
    return pio.to_html(fig, full_html=False, config={'responsive': True})

def crear_imagen_nube_palabras(datos_palabras: List[Tuple[str, int]]) -> str:
    # Convierte la lista de tuplas (palabra, frecuencia) en un diccionario
    diccionario_palabras = dict(datos_palabras)
    
    # Crea la nube de palabras con las frecuencias
    wc = WordCloud(width=800, 
        height=400, 
        background_color='white',
        colormap='viridis',
        relative_scaling=0.5,
        min_font_size=10).generate_from_frequencies(diccionario_palabras)
    
    plt.figure(figsize=(10, 5))
    # Muestra la imagen generada
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('Palabras Más Frecuentes en Reclamos', fontsize=18, pad=20)

    # Guarda la imagen en un archivo
    ruta_imagen = 'static/nube_palabras.png'
    plt.savefig(ruta_imagen, bbox_inches='tight', dpi=100, facecolor='white')
    plt.close()
    # Devuelve una etiqueta HTML para mostrar la imagen
    return f'<img src="{ruta_imagen}" alt="Nube de Palabras">'

def crear_barra_mediana(mediana_en_proceso: float, mediana_resueltos: float, mediana_pendiente: float) -> str:
    """Crea un gráfico de barras con las medianas de tiempos de resolución (días) y devuelve HTML."""
    fig = px.bar(
        x=['Mediana Pendiente','Mediana En Proceso', 'Mediana Resueltos'],
        y=[mediana_pendiente,mediana_en_proceso, mediana_resueltos],
        title='Mediana de Tiempos de Resolución (días)'
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        title_font_size=18,
        showlegend=False,
        xaxis_title='',
        yaxis_title='Días',
        margin=dict(t=60, b=40, l=40, r=20)
    )
    return pio.to_html(fig, full_html=False, config={'responsive': True})

# Prueba simple de las funciones
if __name__ == "__main__":
    # Datos de ejemplo
    datos_torta = {'Resuelto': 60, 'En Proceso': 30, 'Pendiente': 10}
    datos_nube = [('agua', 15), ('luz', 10), ('internet', 8), ('calle', 7), ('basura', 5)]
    mediana_en_proceso = 12.5
    mediana_resueltos = 7.3
    mediana_pendiente = 5.0
    # Guardar los HTML en archivos
    with open("grafico_torta.html", "w", encoding="utf-8") as f:
        f.write(crear_grafico_torta(datos_torta))
    with open("nube_palabras.html", "w", encoding="utf-8") as f:
        f.write(crear_imagen_nube_palabras(datos_nube))
    with open("barra_mediana.html", "w", encoding="utf-8") as f:
        f.write(crear_barra_mediana(mediana_en_proceso, mediana_resueltos, mediana_pendiente))

    print("Archivos HTML generados. Ábrelos con tu navegador para ver los gráficos.")