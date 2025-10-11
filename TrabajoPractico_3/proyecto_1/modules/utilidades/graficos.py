# utilidades/graficos.py
import plotly.express as px
import plotly.io as pio
import numpy as np
from typing import Dict, List, Tuple

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
    return pio.to_html(fig, full_html=False)

def crear_nube_palabras(datos_nube: List[Tuple[str, int]]) -> str:
    """Recibe lista de (palabra, frecuencia) y devuelve HTML para scatter como nube de palabras."""
    if not datos_nube:
        return '<div>No hay datos para mostrar.</div>'
    
    palabras, tamaños = zip(*datos_nube)
    np.random.seed(42)
    x = np.random.rand(len(palabras)).tolist()
    y = np.random.rand(len(palabras)).tolist()
    
    fig = px.scatter(
        x=x, y=y, text=palabras, size=tamaños, color=tamaños,
        color_continuous_scale='viridis',
        title='Palabras Claves en Reclamos (Top 15)'
    )
    fig.update_traces(textposition='top center', marker=dict(line=dict(width=0)))
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False)
    )
    return pio.to_html(fig, full_html=False)

def crear_barra_mediana(mediana_en_proceso: float, mediana_resueltos: float) -> str:
    """Crea un gráfico de barras con las medianas de tiempos de resolución (días) y devuelve HTML."""
    fig = px.bar(
        x=['En Proceso', 'Resueltos'],
        y=[mediana_en_proceso, mediana_resueltos],
        title='Mediana de Tiempos de Resolución (días)'
    )
    return pio.to_html(fig, full_html=False)

# Prueba simple de las funciones
if __name__ == "__main__":
    # Datos de ejemplo
    datos_torta = {'Resuelto': 60, 'En Proceso': 30, 'Pendiente': 10}
    datos_nube = [('agua', 15), ('luz', 10), ('internet', 8), ('calle', 7), ('basura', 5)]
    mediana_en_proceso = 12.5
    mediana_resueltos = 7.3
    # Guardar los HTML en archivos
    with open("grafico_torta.html", "w", encoding="utf-8") as f:
        f.write(crear_grafico_torta(datos_torta))
    with open("nube_palabras.html", "w", encoding="utf-8") as f:
        f.write(crear_nube_palabras(datos_nube))
    with open("barra_mediana.html", "w", encoding="utf-8") as f:
        f.write(crear_barra_mediana(mediana_en_proceso, mediana_resueltos))

    print("Archivos HTML generados. Ábrelos con tu navegador para ver los gráficos.")