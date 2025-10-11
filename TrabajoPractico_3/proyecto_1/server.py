from datetime import datetime
from flask import redirect, render_template, request, url_for, session,flash
from modules.config import app, login_manager
from modules.dominio.usuario import Rol, Claustro
from modules.gestores.gestor_usuario import GestorDeUsuarios
from modules.gestores.gestor_reclamo import GestorDeReclamo
from modules.gestores.gestor_login import GestorDeLogin
import pickle
from modules.comparador_de_reclamos import ComparadorDeReclamos
from modules.factoria import crear_repositorio
from modules.dominio.reclamo import Estado
from flask import flash

usuario_repo, reclamo_repo, departamento_repo = crear_repositorio()

with open('./data/claims_clf.pkl', 'rb') as archivo:
    clf = pickle.load(archivo)

gestor_usuarios = GestorDeUsuarios(usuario_repo, reclamo_repo, clf)
gestor_reclamo = GestorDeReclamo(reclamo_repo, clf)
gestor_login = GestorDeLogin(gestor_usuarios, login_manager, admin_list=[2,3])  # IDs de usuarios administradores
comparador_reclamos = ComparadorDeReclamos()

# Página de inicio
@app.route('/')
def index():
    if gestor_login.usuario_autenticado:
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
        if claustro == "DOCENTE":
            claustro = Claustro.DOCENTE
        elif claustro == "PAYS":
            claustro = Claustro.PAYS
        else:
            claustro = Claustro.ESTUDIANTE
        rol = Rol.USUARIO_FINAL
        
        try:
            gestor_usuarios.crear_usuario(nombre,apellido, email,usuario, password, claustro, rol)
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('error.html', error=str(e))
    return render_template('register.html')

@app.route("/login", methods= ["GET", "POST"])
def login():
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
            if usuario_dominio.rol == Rol.JEFE_DEPARTAMENTO or usuario_dominio.rol == Rol.SECRETARIO_TECNICO:
                return redirect(url_for('manejar_reclamos'))
            return redirect(url_for('crear_reclamo'))
    return render_template('login.html')

@app.route('/crear_reclamo', methods=['GET', 'POST'])
@gestor_login.solo_usuarios_no_admin
def crear_reclamo():
    if request.method == 'POST':
        usuario_id = session['id_usuario']  

        contenido = request.form["input_contenido"]
        timestamp = datetime.now()
        estado = 'PENDIENTE'
        id_departamento = gestor_reclamo.clasificar_reclamo(contenido)

        reclamos = gestor_reclamo.obtener_reclamos_por_departamento_excluir_usuario(id_departamento, usuario_id=usuario_id)
        reclamos = comparador_reclamos.encontrar_reclamos_similares(contenido, reclamos)
        
        # Guardar datos en la sesión de Flask
        session['reclamos'] = [reclamo.to_dict() for reclamo in reclamos]
        session['contenido'] = contenido
        session['timestamp'] = timestamp.isoformat()  # Convertir a string para serializar
        session['estado'] = estado
        session['id_departamento'] = id_departamento

        return redirect(url_for('ver_reclamos_similares'))
    
    return render_template('crear_reclamo.html',active_page='crear_reclamo')

@app.route('/ver_reclamos_similares', methods=['GET', 'POST'])
@gestor_login.se_requiere_login
def ver_reclamos_similares():
    if request.method == 'POST':
        id_reclamo = request.form.get('adherir')
        if id_reclamo:
            try:
                usuario_id = session['id_usuario']  
                gestor_usuarios.adherir_usuario_a_reclamo(usuario_id, id_reclamo)
                #session.clear()  # Limpiar la sesión
                return render_template('confirmacion.html', mensaje="Te has adherido exitosamente al reclamo.")
            except Exception as e:
                return render_template('error.html', error=str(e))
        else:
            usuario_id = session['id_usuario']  
            contenido = session.get('contenido')
            timestamp = datetime.fromisoformat(session.get('timestamp'))
            estado = session.get('estado')
            id_departamento = session.get('id_departamento')
            gestor_reclamo.crear_reclamo(usuario_id, contenido, timestamp, estado, id_departamento)
            #session.clear()  # Limpiar la sesión
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
    reclamos = usuario.obtener_reclamos_creados()
    reclamos_adheridos = usuario.obtener_reclamos_adheridos()
    return render_template('mis_reclamos.html', reclamos=[r.to_dict() for r in reclamos], reclamos_adheridos=[r.to_dict() for r in reclamos_adheridos], active_page='mis_reclamos')

@app.route('/todos_los_reclamos')
@gestor_login.solo_usuarios_no_admin
def todos_los_reclamos():
    reclamos = gestor_reclamo.obtener_todos_los_reclamos()
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

    if jefe.rol == Rol.SECRETARIO_TECNICO:
        datos_reclamos = gestor_reclamo.obtener_todos_los_reclamos()
        datos_reclamos = [r.to_dict() for r in datos_reclamos]
    else:
        datos_reclamos = gestor_reclamo.obtener_reclamos_departamento(id_departamento)
    return render_template('manejar_reclamos.html', datos_reclamos=datos_reclamos, rol=jefe.rol.name)

@app.route('/ayuda')
@gestor_login.admin_only
def ayuda():
    return render_template('ayuda.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
