import plotly.graph_objects as go
import plotly.io as pio


# === Generación de gráficos como objetos Figure ===
def fig_lineas(graficos_procesador):
    grafico_lineas = graficos_procesador.get_time_series_data()
    fig = go.Figure()
    for dataset in grafico_lineas['datasets']:
        fig.add_trace(go.Scatter(
            x=grafico_lineas['labels'],
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


def fig_circular(graficos_procesador):
    grafico_circular = graficos_procesador.get_pie_chart_data()
    fig = go.Figure([go.Pie(
        labels=grafico_circular['labels'],
        values=grafico_circular['data'],
        marker=dict(colors=grafico_circular['backgroundColor'])
    )])
    fig.update_layout(title="Proporción global de aciertos")
    return fig


# === Para HTML (mantienes lo que ya tenías) ===
def grafico_lineas(graficos_procesador):
    fig = fig_lineas(graficos_procesador)  # tu función original
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


def grafico_circular(graficos_procesador):
    fig = fig_circular(graficos_procesador)  # tu función original
    fig.update_layout(
        title_font=dict(color="white"),
        legend=dict(font=dict(color="white")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return pio.to_html(fig, full_html=False)


