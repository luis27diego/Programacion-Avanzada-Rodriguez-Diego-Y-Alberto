import random

class TriviaGame:
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

    def obtener_opciones(self):
        
        frase_correcta_tupla = self.obtener_frase_aleatoria()
        frase_correcta = frase_correcta_tupla[0] # frase (str)
        peli_correcta = frase_correcta_tupla[1]

        opciones = self.obtener_peliculas_aleatorias(2, peli_correcta) 
        opciones.append(peli_correcta)
        random.shuffle(opciones)

        return  {
            'frase': frase_correcta,
            'pelicula_correcta': peli_correcta,
            'opciones': opciones
        }
    def verificar_respuesta(self,question, pelicula_usuario):
        """Verifica si la respuesta del usuario es correcta"""
        return pelicula_usuario.lower() == question['pelicula_correcta'].lower()


""" Mana = TriviaGame()
primer = Mana.obtener_opciones()
print(primer)
print(type(primer))
respuesta = Mana.verificar_respuesta(primer, "El Padrino")
print(respuesta) """
