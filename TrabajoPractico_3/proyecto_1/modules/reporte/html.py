from modules.reporte.reporteABS import ReporteABS
import tempfile
import os
import time
import base64
from flask import send_file


class ReporteHtml(ReporteABS):
    def __init__(self):
        super().__init__()

    def _imagen_a_base64(self, ruta_imagen):
        """Convierte una imagen a base64 para incrustarla en HTML"""
        try:
            with open(ruta_imagen, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                # Detectar tipo de imagen por extensión
                ext = os.path.splitext(ruta_imagen)[1].lower()
                mime_type = 'image/png' if ext == '.png' else 'image/jpeg'
                return f"data:{mime_type};base64,{img_data}"
        except Exception as e:
            print(f"Error al convertir imagen a base64: {e}")
            return None

    def generar_reporte(self, graficos: dict):
        """
        Genera un HTML con imágenes (PNG/JPG) incrustadas en base64 y lo devuelve para web.

        Args:
            graficos: Diccionario con rutas a imágenes:
                - 'figura_torta': ruta a PNG/JPG
                - 'figura_barra_mediana': ruta a PNG/JPG
                - 'figura_nube_palabras': ruta a PNG/JPG
        """
        temp_dir = tempfile.gettempdir()

        # Obtener rutas desde el diccionario (acepta claves nuevas y antiguas)
        ruta_torta = graficos.get('figura_torta')
        ruta_barras =  graficos.get('figura_barra_mediana')
        ruta_nube = graficos.get('figura_nube_palabras')

        # Construir contenido HTML
        html_content = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte de Gráficos</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                h1 {
                    text-align: center;
                    color: #333;
                    border-bottom: 3px solid #4CAF50;
                    padding-bottom: 10px;
                }
                .seccion {
                    background-color: white;
                    margin: 20px 0;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                h2 {
                    color: #4CAF50;
                    margin-top: 0;
                }
                img {
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 10px auto;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <h1>Reporte de Gráficos</h1>
        """

        # Agregar secciones con imágenes si las rutas existen
        if ruta_torta and os.path.exists(ruta_torta):
            img_base64 = self._imagen_a_base64(ruta_torta)
            if img_base64:
                html_content += f"""
            <div class="seccion">
                <h2>Gráfico de Torta</h2>
                <img src="{img_base64}" alt="Gráfico de Torta">
            </div>
                """

        if ruta_nube and os.path.exists(ruta_nube):
            img_base64 = self._imagen_a_base64(ruta_nube)
            if img_base64:
                html_content += f"""
            <div class="seccion">
                <h2>Nube de Palabras</h2>
                <img src="{img_base64}" alt="Nube de Palabras">
            </div>
                """

        if ruta_barras and os.path.exists(ruta_barras):
            img_base64 = self._imagen_a_base64(ruta_barras)
            if img_base64:
                html_content += f"""
            <div class="seccion">
                <h2>Gráfico de Barras</h2>
                <img src="{img_base64}" alt="Gráfico de Barras">
            </div>
                """

        # Cerrar HTML
        html_content += """
        </body>
        </html>
        """

        # Guardar HTML en carpeta temporal (nombre único para evitar colisiones)
        temp_html = os.path.join(temp_dir, f'reporte_graficos_{int(time.time())}.html')
        
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Enviar HTML directamente al cliente
        return send_file(temp_html, as_attachment=True, download_name='reporte_graficos.html')