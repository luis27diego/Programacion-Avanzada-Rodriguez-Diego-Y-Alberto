from datetime import datetime
from flask import redirect, render_template, request, url_for, session,flash
from modules.config import app, login_manager
from modules.gestores.gestor_usuario import GestorDeUsuarios
from modules.gestores.gestor_reclamo import GestorDeReclamo
from modules.gestores.gestor_login import GestorDeLogin
from modules.gestores.dashboardService import DashboardService
from modules.gestores.gestor_dashboard import GestorDashboard
import pickle
from modules.factoria import crear_repositorio, crear_reporte   
from modules.dominio.reclamo import Estado
from modules.utilidades.comparador_de_reclamos import ComparadorDeReclamos 

usuario_repo, reclamo_repo, departamento_repo, adhesion_repo = crear_repositorio()

with open('./data/claims_clf.pkl', 'rb') as archivo:
    clf = pickle.load(archivo)

comparador_reclamos = ComparadorDeReclamos()
gestor_usuarios = GestorDeUsuarios(usuario_repo)
gestor_reclamo = GestorDeReclamo(reclamo_repo, usuario_repo, adhesion_repo)
gestor_login = GestorDeLogin(gestor_usuarios, login_manager)  # IDs de usuarios administradores
dashboard_service = DashboardService(usuario_repo,reclamo_repo) 
# Página de inicio
@app.route('/')
def index():
    if gestor_login.es_admin:
        return redirect(url_for('manejar_reclamos'))
    elif gestor_login.usuario_autenticado:
        return redirect(url_for('crear_reclamo'))
    return redirect(url_for('login'))

@app.route("/register", methods= ["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["input_nombre"]
        apellido = request.form["input_apellido"]
        usuario = request.form["input_usuario"]
        email = request.form["input_email"]
        password = request.form["input_password"]
        claustro = request.form["input_claustro"]

        try:
            gestor_usuarios.crear_usuario(nombre,apellido, email,usuario, password, claustro)
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e))
            return render_template('register.html')
    return render_template('register.html')

@app.route("/login", methods= ["GET", "POST"])
def login():
    if gestor_login.usuario_autenticado:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        email = request.form["input_email"]
        password = request.form["input_password"]
        try :
            usuario_dominio = gestor_usuarios.autenticar_usuario(email, password)
        except Exception as e:
            flash(str(e))  # Cambiar esta línea
            return render_template('login.html')  # Y agregar esta línea
        if usuario_dominio:
            gestor_login.login_usuario(usuario_dominio)
            session['id_usuario'] = usuario_dominio.id  # Guardar el ID del usuario en la sesión
            if hasattr(usuario_dominio, 'rol'):
                 return redirect(url_for('manejar_reclamos'))
            return redirect(url_for('crear_reclamo'))
    return render_template('login.html')

@app.route('/crear_reclamo', methods=['GET', 'POST'])
@gestor_login.solo_usuarios_no_admin
def crear_reclamo():
    for key in ('contenido', 'timestamp', 'estado', 'id_departamento'):
        session.pop(key, None)

    if request.method == 'POST':
        usuario_id = session['id_usuario']  

        contenido = request.form["input_contenido"]
        timestamp = datetime.now()
        estado = 'PENDIENTE'
        id_departamento = gestor_reclamo.clasificar_reclamo(contenido, clf)
        reclamos = gestor_reclamo.obtener_reclamos_por_departamento_excluir_usuario(id_departamento, usuario_id=usuario_id)
        reclamos = gestor_reclamo.encontrar_reclamos_similares(contenido, reclamos, comparador_reclamos)

        # Guardar datos en la sesión de Flask
        session['reclamos'] = [reclamo.to_dict() for reclamo in reclamos]
        session['contenido'] = contenido
        session['timestamp'] = timestamp.isoformat()  # Convertir a string para serializar
        session['estado'] = estado
        session['id_departamento'] = id_departamento

        return redirect(url_for('ver_reclamos_similares'))
    
    return render_template('crear_reclamo.html',active_page='crear_reclamo')

@app.route('/ver_reclamos_similares', methods=['GET', 'POST'])
@gestor_login.solo_usuarios_no_admin
def ver_reclamos_similares():

    # Verificar que hay un reclamo en proceso
    if not session.get('contenido') or not session.get('timestamp') or not session.get('estado') or not session.get('id_departamento'):
        flash("No hay un reclamo en proceso. Por favor, crea un reclamo primero.", "error")
        return redirect(url_for('crear_reclamo'))

    if request.method == 'POST':
        id_reclamo = request.form.get('adherir')
        if id_reclamo:
            try:
                usuario_id = session['id_usuario']  
                #gestor_usuarios.adherir_usuario_a_reclamo(usuario_id, id_reclamo)
                gestor_reclamo.adherir_usuario_a_reclamo(usuario_id, int(id_reclamo))
                for key in ('contenido', 'timestamp', 'estado', 'id_departamento'):
                    session.pop(key, None)
                return render_template('confirmacion.html', mensaje="Te has adherido exitosamente al reclamo.")
            except Exception as e:
                flash(str(e))
                return render_template('crear_reclamo.html')
        else:
            usuario_id = session['id_usuario']  
            contenido = session.get('contenido')
            timestamp = datetime.fromisoformat(session.get('timestamp'))
            estado = session.get('estado')
            id_departamento = session.get('id_departamento')
            gestor_reclamo.crear_reclamo(usuario_id, contenido, timestamp, estado, id_departamento)
            # Limpiar sólo los campos del reclamo, manteniendo id_usuario en sesión
            for key in ('contenido', 'timestamp', 'estado', 'id_departamento'):
                session.pop(key, None)
            return render_template('confirmacion.html', mensaje="El reclamo ha sido creado exitosamente.")
    
    # Obtener datos de la sesión de Flask
    reclamos = session.get('reclamos', [])
    return render_template('ver_reclamos_similares.html', reclamos=reclamos)

# Ruta para mostrar reclamos del usuario
@app.route('/mis_reclamos')
@gestor_login.solo_usuarios_no_admin
def mis_reclamos():
    print(session['id_usuario'])
    #reclamos = gestor_usuarios.obtener_reclamos_creados_por_usuario(session['id_usuario'])
    usuario = gestor_usuarios.obtener_usuario_por_id(session['id_usuario'])
    #reclamos = usuario.obtener_reclamos_creados() 
    reclamos = gestor_reclamo.obtener_reclamos_creados_por_usuario(session['id_usuario'])
    #reclamos_adheridos = usuario.obtener_reclamos_adheridos()
    reclamos_adheridos = gestor_reclamo.obtener_reclamos_adheridos_por_usuario(session['id_usuario'])
    return render_template('mis_reclamos.html', reclamos=[r.to_dict() for r in reclamos], reclamos_adheridos=[r.to_dict() for r in reclamos_adheridos], active_page='mis_reclamos')

@app.route('/todos_los_reclamos', methods=['GET', 'POST'])
@gestor_login.solo_usuarios_no_admin
def todos_los_reclamos():
    if request.method == 'POST':
        departamento_seleccionado = request.form.get('departamento')

        if departamento_seleccionado is None or departamento_seleccionado == '':
            pass

        else:
            reclamos = gestor_reclamo.obtener_reclamos_por_estado(Estado.PENDIENTE)
            reclamos = [r for r in reclamos if r.departamento_id == int(departamento_seleccionado)]
            return render_template('todos_los_reclamos.html', reclamos=[r.to_dict() for r in reclamos], active_page='todos_los_reclamos', departamento_seleccionado=departamento_seleccionado)

    reclamos = gestor_reclamo.obtener_reclamos_por_estado(Estado.PENDIENTE)
    return render_template('todos_los_reclamos.html', reclamos=[r.to_dict() for r in reclamos], active_page='todos_los_reclamos')


@app.route("/logout")
def logout():    
    gestor_login.logout_usuario()      
    return redirect(url_for('login'))

@app.route('/manejar_reclamos', methods=['GET', 'POST'])
@gestor_login.admin_only
def manejar_reclamos():
    jefe = gestor_usuarios.obtener_usuario_por_id(session['id_usuario'])
    id_departamento = jefe.departamento_id

    if request.method == 'POST':
        id_reclamo = request.form.get('id_reclamo')
        estado = request.form.get('estado')
        nuevo_departamento = request.form.get('nuevo_departamento')  # Solo si el rol es SECRETARIO_TECNICO
        if not id_reclamo:
            flash("ID del reclamo no proporcionado.", "error")
            return redirect(url_for('manejar_reclamos'))
        try:
            id_reclamo = int(id_reclamo)
        except ValueError:
            flash("ID del reclamo inválido.", "error")
            return redirect(url_for('manejar_reclamos'))

        # Obtener el reclamo actual para comparar
        reclamo_actual = gestor_reclamo.obtener_reclamo_por_id(id_reclamo)
        if not reclamo_actual:
            flash("Reclamo no encontrado.", "error")
            return redirect(url_for('manejar_reclamos'))

        # Verificar y actualizar estado solo si cambió
        if estado and estado in ["INVALIDO", "PENDIENTE", "EN_PROCESO", "RESUELTO"]:
            estado_map = {
                "INVALIDO": Estado.INVALIDO,
                "PENDIENTE": Estado.PENDIENTE,
                "EN_PROCESO": Estado.EN_PROCESO,
                "RESUELTO": Estado.RESUELTO
            }
            nuevo_estado = estado_map[estado]
            
            if reclamo_actual.estado != nuevo_estado:  # Comparar con el estado actual
                print(nuevo_estado,reclamo_actual.estado)
                gestor_reclamo.modificar_estado_reclamo(id_reclamo, nuevo_estado)
                flash("Reclamo actualizado correctamente.", "success")

        # Verificar y actualizar departamento solo si cambió
        if nuevo_departamento:
            try:
                nuevo_departamento_id = int(nuevo_departamento)
                if reclamo_actual.departamento_id != nuevo_departamento_id:  # Comparar con el departamento actual
                    gestor_reclamo.modificar_departamento_reclamo(id_reclamo, nuevo_departamento_id)
                    flash("Departamento cambiado correctamente.", "success")

            except ValueError:
                flash("Departamento inválido.", "error")
                return redirect(url_for('manejar_reclamos'))
            except Exception as e:
                flash(str(e), "error")
                return redirect(url_for('manejar_reclamos'))

        return redirect(url_for('manejar_reclamos'))

    if jefe.rol == 'SECRETARIO_TECNICO':
        datos_reclamos = gestor_reclamo.obtener_todos_los_reclamos()
        datos_reclamos = [r.to_dict() for r in datos_reclamos]
    else:
        datos_reclamos = gestor_reclamo.obtener_reclamos_departamento(id_departamento)
        datos_reclamos = [r.to_dict() for r in datos_reclamos]
    return render_template('manejar_reclamos.html', datos_reclamos=datos_reclamos, rol=jefe.rol, active_page='manejar_reclamos')
 
@app.route('/dashboard')
@gestor_login.admin_only
def dashboard():
    gestor_dashboard = GestorDashboard(dashboard_service)
    jefe = gestor_usuarios.obtener_usuario_por_id(session['id_usuario'])
    id_departamento = jefe.departamento_id
    grafico_torta = gestor_dashboard.generar_grafico_torta(id_departamento, session['id_usuario'])
    grafico_barras_mediana = gestor_dashboard.generar_barra_mediana(id_departamento, session['id_usuario'])
    html_nube = gestor_dashboard.generar_imagen_nube_palabras(id_departamento, session['id_usuario'])

    return render_template('dashboard.html', grafico_torta=grafico_torta, grafico_barras_mediana=grafico_barras_mediana, nube_palabras=html_nube,  active_page='dashboard')


@app.route('/dashboard/reporte')
@gestor_login.admin_only
def descargar_reporte():
    gestor_dashboard = GestorDashboard(dashboard_service)
    jefe = gestor_usuarios.obtener_usuario_por_id(session['id_usuario'])
    id_departamento = jefe.departamento_id
    formato = request.args.get("formato", "pdf")  # Por defecto PDF
    reporte = crear_reporte(formato)
    reporte = gestor_dashboard.generar_reporte(reporte, id_departamento, session['id_usuario'])

    return reporte

@app.route('/ayuda')
@gestor_login.admin_only
def ayuda():
    return render_template('ayuda.html',active_page='ayuda')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    