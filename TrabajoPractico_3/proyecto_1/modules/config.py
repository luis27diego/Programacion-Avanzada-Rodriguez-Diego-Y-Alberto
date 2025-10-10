from datetime import timedelta
from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_session import Session
from pathlib import Path # Para manejar rutas de archivos


app = Flask("server")
app.config['secret_key'] ='1234'


BASE_DIR = Path(__file__).resolve().parent.parent  # para poder acceder desde cualquier lugar a la ruta de la base de datos
urlBD = f"sqlite:///{BASE_DIR / 'database.db'}"

def crear_engine():
    engine = create_engine(urlBD)
    Session = sessionmaker(bind=engine)
    return Session

app.config.from_object(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)
Session(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)