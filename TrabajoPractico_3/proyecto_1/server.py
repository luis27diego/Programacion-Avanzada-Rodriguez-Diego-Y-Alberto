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

usuario_repo, reclamo_repo, departamento_repo = crear_repositorio()

with open('./data/claims_clf.pkl', 'rb') as archivo:
    clf = pickle.load(archivo)

gestor_usuarios = GestorDeUsuarios(usuario_repo, reclamo_repo, clf)
gestor_reclamo = GestorDeReclamo(reclamo_repo, clf)
gestor_login = GestorDeLogin(gestor_usuarios, login_manager, admin_list=['admin'])
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
            return redirect(url_for('crear_reclamo'))
        else:
            return render_template('error.html', error="Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/crear_reclamo', methods=['GET', 'POST'])
@gestor_login.se_requiere_login
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
    
    return render_template('crear_reclamo.html')

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
@gestor_login.se_requiere_login
def mis_reclamos():
    print(session['id_usuario'])
    #reclamos = gestor_usuarios.obtener_reclamos_creados_por_usuario(session['id_usuario'])
    usuario = gestor_usuarios.obtener_usuario_por_id(session['id_usuario'])
    reclamos = usuario.obtener_reclamos_creados()
    reclamos_adheridos = usuario.obtener_reclamos_adheridos()
    return render_template('mis_reclamos.html', reclamos=[r.to_dict() for r in reclamos], reclamos_adheridos=[r.to_dict() for r in reclamos_adheridos])

@app.route('/todos_los_reclamos')
@gestor_login.se_requiere_login
def todos_los_reclamos():
    reclamos = gestor_reclamo.obtener_todos_los_reclamos()
    return render_template('todos_los_reclamos.html', reclamos=[r.to_dict() for r in reclamos])


@app.route("/logout")
def logout():    
    gestor_login.logout_usuario()      
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
