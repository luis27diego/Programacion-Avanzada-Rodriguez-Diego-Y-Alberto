import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt


# === Generación de gráficos como objetos Figure ===
def fig_lineas(datos_lineas):
    fig = go.Figure()
    for dataset in datos_lineas['datasets']:
        fig.add_trace(go.Scatter(
            x=datos_lineas['labels'],
            y=dataset['data'],
            mode='lines+markers',
            name=dataset['label'],
            line=dict(color=dataset['borderColor']),
            marker=dict(color=dataset['borderColor'])
        ))
    fig.update_layout(title="Evolución de aciertos y desaciertos",
                      xaxis_title="Fecha y Hora",
                      yaxis_title="Cantidad de respuestas",
                      )
    fig.update_xaxes(type="category")

    return fig


def fig_circular(datos_circular):
    fig = go.Figure([go.Pie(
        labels=datos_circular['labels'],
        values=datos_circular['data'],
        marker=dict(colors=datos_circular['backgroundColor'])
    )])
    fig.update_layout(title="Proporción global de aciertos")
    return fig

def fig_circular_matplotlib(datos_circular, filename="static/grafico_circular.png"):
    """
    Genera un gráfico de torta usando matplotlib a partir de los datos circulares y lo guarda como PNG en la carpeta static.
    """
    labels = datos_circular['labels']
    values = datos_circular['data']
    colors = ['#22c55e', '#ef4444', '#3b82f6', '#f59e42', '#a855f7', '#fbbf24']

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title("Proporción global de aciertos")
    ax.axis('equal')  # Para que el gráfico sea circular

    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig)
    return filename

# === Para HTML (mantienes lo que ya tenías) ===
def grafico_lineas(datos_lineas):
    fig = fig_lineas(datos_lineas)  # tu función original
    # Aplicar colores solo para HTML
    fig.update_layout(
        title_font=dict(color="white"),
        xaxis=dict(
            tickfont=dict(color="white"),
            title_font=dict(color="white"),
            showgrid=False
        ),
        yaxis=dict(
            tickfont=dict(color="white"),
            title_font=dict(color="white"),
            showgrid=False
        ),
        legend=dict(font=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return pio.to_html(fig, full_html=False)


def grafico_circular(datos_circular):
    fig = fig_circular(datos_circular)  # tu función original
    fig.update_layout(
        title_font=dict(color="white"),
        legend=dict(font=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return pio.to_html(fig, full_html=False)


