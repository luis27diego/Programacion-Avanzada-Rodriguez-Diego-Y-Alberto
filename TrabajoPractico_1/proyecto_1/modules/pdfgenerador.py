from fpdf import FPDF
import tempfile
import os
from flask import send_file
import kaleido
from modules.GeneraciondDeGraficos import fig_circular, fig_lineas
import  time

#funcion para evitar error de kaleido en windows (descarga un chorme para poder convertir a imagen)
#kaleido.get_chrome_sync()



def generar_pdf(graficos_procesador):
    temp_dir = tempfile.gettempdir()

    img_lineas = os.path.join(temp_dir, 'grafico_lineas.png')
    img_circular = os.path.join(temp_dir, 'grafico_circular.png')

    # Usamos las funciones que devuelven figuras
    fig_lineas(graficos_procesador).write_image(img_lineas)
    time.sleep(0.1)  # darle tiempo a Windows a soltar el archivo
    fig_circular(graficos_procesador).write_image(img_circular)
    time.sleep(0.1)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte de Resultados Históricos', ln=True, align='C')

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Evolución de Aciertos y Desaciertos', ln=True)
    pdf.image(img_lineas, w=180)
    pdf.ln(10)
    pdf.cell(0, 10, 'Proporción Global de Aciertos', ln=True)
    pdf.image(img_circular, w=120)

    temp_pdf = os.path.join(temp_dir, 'resultados_historicos.pdf')
    pdf.output(temp_pdf)

    # Eliminar imágenes temporales
    os.remove(img_lineas)
    os.remove(img_circular)

    return send_file(temp_pdf, as_attachment=True, download_name='resultados_historicos.pdf')
