from modules.gestores.dashboardService import DashboardService
from modules.reporte.reporteABS import ReporteABS
from modules.utilidades.graficos import crear_grafico_torta, crear_imagen_nube_palabras, crear_barra_mediana,crear_figura_barra_mediana, crear_figura_nube_palabras, crear_figura_torta


class GestorDashboard:
    def __init__(self, dashboard_service):
        self.dashboard_service = dashboard_service

    def obtener_analiticas(self, id_departamento, id_usuario):
        return self.dashboard_service.obtener_analiticas(id_departamento, id_usuario)

    def generar_grafico_torta(self, id_departamento, id_usuario):
        datos = self.obtener_analiticas(id_departamento, id_usuario)
        return crear_grafico_torta(datos['datos_torta'])

    def generar_imagen_nube_palabras(self, id_departamento, id_usuario):
        datos = self.obtener_analiticas(id_departamento, id_usuario)
        return crear_imagen_nube_palabras(datos['datos_nube_palabras'])

    def generar_barra_mediana(self, id_departamento, id_usuario):
        datos = self.obtener_analiticas(id_departamento, id_usuario)
        return crear_barra_mediana(datos['mediana_en_proceso'], datos['mediana_resolucion'],
                                   datos['mediana_pendiente'])



    def generar_figura_barra_mediana(self, id_departamento, id_usuario):
        datos = self.obtener_analiticas(id_departamento, id_usuario)
        return crear_figura_barra_mediana(datos['mediana_en_proceso'], datos['mediana_resolucion'],
                                   datos['mediana_pendiente'])
    
    def generar_figura_torta(self, id_departamento, id_usuario):
        datos = self.obtener_analiticas(id_departamento, id_usuario)
        return crear_figura_torta(datos['datos_torta'])
    
    def generar_figura_nube_palabras(self, id_departamento, id_usuario):
        datos = self.obtener_analiticas(id_departamento, id_usuario)
        return crear_figura_nube_palabras(datos['datos_nube_palabras'])


    def generar_reporte(self, reporte: ReporteABS, id_departamento, id_usuario):
        graficos = {
            'figura_torta': self.generar_figura_torta(id_departamento, id_usuario),
            'figura_nube_palabras': self.generar_figura_nube_palabras(id_departamento, id_usuario),
            'figura_barra_mediana': self.generar_figura_barra_mediana(id_departamento, id_usuario)
        }
        return reporte.generar_reporte(graficos)


if __name__ == "__main__":

    from modules.factoria import crear_repositorio, crear_reporte

    usuario_repo, reclamo_repo, departamento_repo = crear_repositorio()
    dashboard_service = DashboardService(usuario_repo, reclamo_repo)
    reporte = crear_reporte('pdf')
    gestor_dashboard = GestorDashboard(dashboard_service, reporte)

    analiticas = gestor_dashboard.obtener_analiticas(id_departamento=1, id_usuario=1)
    print(analiticas)
    grafico_torta = gestor_dashboard.generar_grafico_torta(id_departamento=1, id_usuario=1)
    imagen_nube_palabras = gestor_dashboard.generar_imagen_nube_palabras(id_departamento=1, id_usuario=1)
    barra_mediana = gestor_dashboard.generar_barra_mediana(id_departamento=1, id_usuario=1)
    # resultado_reporte = gestor_dashboard.generar_reporte(tipo='pdf', id_departamento=1, id_usuario=1)
    # print(resultado_reporte)