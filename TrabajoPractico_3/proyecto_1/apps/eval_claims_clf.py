import pickle

# Abrir el archivo con el clasificador y guardarlo en la variable clf
with open('./data/claims_clf.pkl', 'rb') as archivo:
    clf  = pickle.load(archivo)

# Ahora en clf tenemos el clasificador entrenado

# Ejemplos de reclamos a clasificar
claims = [
    "La computadora 1 del laboratorio 3 no enciende", 
    "El proyector del aula 2 no proyecta la imagen", 
    "El piso del aula 5 está muy sucio", 
    "No puedo enviar mi trabajo por correo electrónico porque la red no funciona",
    "El pizarrón del aula 4 está roto",
    "La impresora de la biblioteca no imprime",
    "El aire acondicionado del aula 1 no enfría",
    "El baño de la planta baja está inundado",
]

# En los ejemplos siguientes, tener presente que 
# el método `classify()` recibe como parámetro una 
# lista de reclamos (lista de strings).

# Clasificar varios reclamos
print(clf.classify(claims))

# Clasificar un reclamo
print(clf.classify(["El proyector del aula 7 no proyecta la imagen"]))