# modules/validaciones.py
def validar_nombre_y_numero_frases(nombre: str, n_frases: int):
    """
    Valida los parámetros de entrada para iniciar el juego.
    """
    nombre = (nombre or "").strip()
    if not nombre:
        return False, "Ingresá tu nombre de usuario."

    if n_frases < 3:
        return False, "El número de frases debe ser al menos 3."

    return True, {"nombre": nombre, "n": n_frases}