from .Frutas import Kiwi, Manzana
from .Verduras import Papa, Zanahoria

def crear_alimento(tipo, peso):
    """Crea una instancia del alimento correspondiente según el tipo."""
    tipo = tipo.lower()
    if tipo == "kiwi":
        return Kiwi(peso)
    elif tipo == "manzana":
        return Manzana(peso)
    elif tipo == "papa":
        return Papa(peso)
    elif tipo == "zanahoria":
        return Zanahoria(peso)
    else:
        raise ValueError(f"Tipo de alimento no reconocido: {tipo}")