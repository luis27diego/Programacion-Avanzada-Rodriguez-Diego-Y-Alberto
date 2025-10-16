from modules.reporte.reporteABS import ReporteABS
from fpdf import FPDF
import tempfile
import os
import time
import shutil
from flask import send_file


class ReportePDF(ReporteABS):
    def __init__(self):
        super().__init__()

    def generar_reporte(self, graficos: dict):
        """
        Genera un PDF solo con gráficos y sus títulos y lo devuelve para web.
        
        Args:
            graficos: Diccionario con las FIGURAS:
                - 'grafico_torta': Figura de Plotly
                - 'grafico_barras': Figura de Plotly
                - 'imagen_nube_palabras': Ruta al archivo PNG o figura matplotlib
        """
        temp_dir = tempfile.gettempdir()
        
        # Rutas temporales para las imágenes
        img_torta = os.path.join(temp_dir, 'grafico_torta.png')
        img_nube = os.path.join(temp_dir, 'nube_palabras.png')
        img_barras = os.path.join(temp_dir, 'grafico_barras.png')
        
        # Convertir figuras a PNG
        fig_torta = graficos.get('figura_torta')
        if fig_torta:
            fig_torta.write_image(img_torta)
            print("Gráfico de torta guardado en:", img_torta)
            time.sleep(0.1)
        
        fig_nube = graficos.get('figura_nube_palabras')
        if fig_nube:
            if hasattr(fig_nube, 'savefig'):  # matplotlib
                fig_nube.savefig(img_nube, bbox_inches='tight', dpi=100, facecolor='white')
                import matplotlib.pyplot as plt
                plt.close(fig_nube)
                time.sleep(0.1)
            elif isinstance(fig_nube, str) and os.path.exists(fig_nube):
                shutil.copy(fig_nube, img_nube)
        
        fig_barras = graficos.get('figura_barra_mediana')
        if fig_barras:
            fig_barras.write_image(img_barras)
            time.sleep(0.1)
        
        # Crear PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Reporte de Gráficos', ln=True, align='C')
        pdf.ln(5)
        
        # Agregar gráficos con título
        if os.path.exists(img_torta):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Gráfico de Torta', ln=True)
            pdf.image(img_torta, w=150)
            pdf.ln(5)
        
        if os.path.exists(img_nube):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Nube de Palabras', ln=True)
            pdf.image(img_nube, w=150)
            pdf.ln(5)
        
        if os.path.exists(img_barras):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Gráfico de Barras', ln=True)
            pdf.image(img_barras, w=150)
        
        # Guardar PDF en carpeta temporal
        temp_pdf = os.path.join(temp_dir, 'reporte_graficos.pdf')
        pdf.output(temp_pdf)

        # Eliminar imágenes temporales
        if os.path.exists(img_torta):
            os.remove(img_torta)
        if os.path.exists(img_nube):
            os.remove(img_nube)
        if os.path.exists(img_barras):
            os.remove(img_barras)
        # NO BORRAR las imágenes todavía; Flask necesita leerlas
        # Enviar PDF directamente al cliente
        return send_file(temp_pdf, as_attachment=True, download_name='reporte_graficos.pdf')
