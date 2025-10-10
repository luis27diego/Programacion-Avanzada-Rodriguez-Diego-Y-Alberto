from datetime import datetime
from flask import redirect, render_template, request, url_for, session
from modules.config import app
from modules.gestores.gestor_usuario import GestorDeUsuarios
from modules.gestores.gestor_reclamo import GestorDeReclamo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.repositorioConcreto.usuario_concreto import UsuarioRepositorio
from modules.repositorioConcreto.reclamo_concreto import ReclamoRepositorio
import pickle
from modules.comparador_de_reclamos import ComparadorDeReclamos

# Configurar clave secreta para sesiones
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave segura en producción

engine = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()  # Renombrado a db_session para evitar conflicto

usuario_repo = UsuarioRepositorio(db_session)
reclamo_repo = ReclamoRepositorio(db_session)
with open('./data/claims_clf.pkl', 'rb') as archivo:
    clf = pickle.load(archivo)

gestor_usuarios = GestorDeUsuarios(usuario_repo, reclamo_repo, clf)
gestor_reclamo = GestorDeReclamo(reclamo_repo, clf)
comparador_reclamos = ComparadorDeReclamos()

# Página de inicio
@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/crear_reclamo', methods=['GET', 'POST'])
def crear_reclamo():
    if request.method == 'POST':
        usuario_id = 4  # Placeholder, reemplazar con autenticación

        contenido = request.form["input_nombre"]
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
def ver_reclamos_similares():
    if request.method == 'POST':
        id_reclamo = request.form.get('adherir')
        if id_reclamo:
            try:
                usuario_id = 4   # Placeholder, reemplazar con autenticación
                gestor_usuarios.adherir_usuario_a_reclamo(usuario_id, id_reclamo)
                session.clear()  # Limpiar la sesión
                return render_template('confirmacion.html', mensaje="Te has adherido exitosamente al reclamo.")
            except Exception as e:
                return render_template('error.html', error=str(e))
        else:
            usuario_id = 4  # Placeholder, reemplazar con autenticación
            contenido = session.get('contenido')
            timestamp = datetime.fromisoformat(session.get('timestamp'))
            estado = session.get('estado')
            id_departamento = session.get('id_departamento')
            gestor_reclamo.crear_reclamo(usuario_id, contenido, timestamp, estado, id_departamento)
            session.clear()  # Limpiar la sesión
            return render_template('confirmacion.html', mensaje="El reclamo ha sido creado exitosamente.")
    
    # Obtener datos de la sesión de Flask
    reclamos = session.get('reclamos', [])
    return render_template('ver_reclamos_similares.html', reclamos=reclamos)

# Ruta para mostrar reclamos del usuario
@app.route('/mis_reclamos')
def mis_reclamos():
    reclamos = gestor_usuarios.obtener_reclamos_creados_por_usuario(1)  # Placeholder, reemplazar con autenticación
    return render_template('mis_reclamos.html', reclamos=[r.to_dict() for r in reclamos])

@app.route('/todos_los_reclamos')
def todos_los_reclamos():
    reclamos = gestor_reclamo.obtener_todos_los_reclamos()
    return render_template('todos_los_reclamos.html', reclamos=[r.to_dict() for r in reclamos])
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
