import random

class PeliManager:
    def __init__(self,datafile: str = "data/frases_de_peliculas.txt"):
        self.data_file = datafile
        self.frases_peliculas = []  # Lista de tuplas (frase, pelicula)
        self.peliculas_unicas = []  # Lista de películas únicas ordenadas
        self.contador = 0
        self.carga_peliculas()
        

    def carga_peliculas(self):
        """
        Carga el archivo y procesa las frases y películas.
        """
        with open(self.data_file, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                self.contador += 1
                linea = linea.strip()
                if linea:  # Si la línea no está vacía
                    frase, pelicula = linea.split(';')
                    self.frases_peliculas.append((frase, pelicula))
        
        # Obtener películas únicas y ordenarlas
        peliculas_set = set()
        for frase, pelicula in self.frases_peliculas:
            peliculas_set.add(pelicula)
        
        self.peliculas_unicas = sorted(list(peliculas_set))
    

    def obtener_peliculas_ordenadas(self):
        """
        Devuelve la lista de películas únicas ordenadas alfabéticamente.
        """
        return self.peliculas_unicas
    
    def obtener_peliculas_indexeada(self):
        """
        Devuelve la lista de películas únicas ordenadas alfabéticamente y indexeada.
        """
        diccionario = {}
        for i, peliculas in enumerate(self.peliculas_unicas):
             diccionario[i + 1] = peliculas
             
        return diccionario

    def obtener_frase_aleatoria(self):
        """
        Devuelve una tupla (frase, pelicula) aleatoria.
        """
        return random.choice(self.frases_peliculas)
    
    def obtener_peliculas_aleatorias(self, cantidad, excluir_pelicula):
        """
        Devuelve una lista de películas aleatorias excluyendo una película específica.
        """
        peliculas_disponibles = [p for p in self.peliculas_unicas if p != excluir_pelicula]
        return random.sample(peliculas_disponibles, cantidad)


manager = PeliManager()
# Para mostrar todas las películas
peliculas = manager.frases_peliculas
print(len(peliculas))
print(manager.contador)
print("********************************************************************************************")
peliculas_unicas = manager.peliculas_unicas
print(len(peliculas_unicas))
print(manager.obtener_peliculas_indexeada())