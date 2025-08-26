# gestor.py
class GestorUsuarios:
    def __init__(self):
        self.usuarios = []

    def agregar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def obtener_usuarios(self):
        return self.usuarios
