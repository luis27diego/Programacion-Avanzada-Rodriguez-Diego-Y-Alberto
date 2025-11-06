from modules.reporte.reporteABS import ReporteABS
from fpdf import FPDF
import tempfile
import os
import time
from flask import send_file


class ReportePDF(ReporteABS):
    def __init__(self):
        super().__init__()

    def generar_reporte(self, graficos: dict):
        """
        Genera un PDF solo con imágenes (PNG/JPG) y sus títulos y lo devuelve para web.

        Args:
            graficos: Diccionario con rutas a imágenes:
                - 'ruta_torta' | 'grafico_torta' | 'figura_torta': ruta a PNG/JPG
                - 'ruta_barras' | 'grafico_barras' | 'figura_barra_mediana': ruta a PNG/JPG
                - 'ruta_nube_palabras' | 'imagen_nube_palabras' | 'figura_nube_palabras': ruta a PNG/JPG
        """
        temp_dir = tempfile.gettempdir()

        # Obtener rutas desde el diccionario (acepta claves nuevas y antiguas)
        ruta_torta = graficos.get('ruta_torta') or graficos.get('grafico_torta') or graficos.get('figura_torta')
        ruta_barras = graficos.get('ruta_barras') or graficos.get('grafico_barras') or graficos.get('figura_barra_mediana')
        ruta_nube = graficos.get('ruta_nube_palabras') or graficos.get('imagen_nube_palabras') or graficos.get('figura_nube_palabras')

        # Crear PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Reporte de Gráficos', ln=True, align='C')
        pdf.ln(5)

        # Agregar imágenes si las rutas existen
        if ruta_torta and os.path.exists(ruta_torta):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Gráfico de Torta', ln=True)
            pdf.image(ruta_torta, w=150)
            pdf.ln(5)

        if ruta_nube and os.path.exists(ruta_nube):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Nube de Palabras', ln=True)
            pdf.image(ruta_nube, w=150)
            pdf.ln(5)

        if ruta_barras and os.path.exists(ruta_barras):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Gráfico de Barras', ln=True)
            pdf.image(ruta_barras, w=150)

        # Guardar PDF en carpeta temporal (nombre único para evitar colisiones)
        temp_pdf = os.path.join(temp_dir, f'reporte_graficos_{int(time.time())}.pdf')
        pdf.output(temp_pdf)

        # Enviar PDF directamente al cliente
        return send_file(temp_pdf, as_attachment=True, download_name='reporte_graficos.pdf')