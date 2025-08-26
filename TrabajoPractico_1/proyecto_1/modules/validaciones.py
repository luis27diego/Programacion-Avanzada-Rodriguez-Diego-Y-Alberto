# modules/validaciones.py
def validar_parametros(nombre: str, n_frases_str: str):
    nombre = (nombre or "").strip()
    if not nombre:
        return False, "Ingresá tu nombre de usuario."

    try:
        n = int(n_frases_str)
    except ValueError:
        return False, "Ingresá un número válido de frases (≥ 3)."

    if n < 3:
        return False, "El número de frases debe ser al menos 3."

    return True, {"nombre": nombre, "n": n}
