from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
from modules.dominio.reclamo import ReclamoDominio
from abc import ABC, abstractmethod

# Descargar recursos de NLTK si no los tienes
nltk.download('stopwords',quiet=True)
nltk.download('punkt',quiet=True)
class ComparadorDeReclamosABC(ABC):
    @abstractmethod
    def encontrar_reclamos_similares(self, nuevo_contenido: str, reclamos_existentes: List[ReclamoDominio], umbral: float = 0.7, top_n: int = 5) :
        pass

class ComparadorDeReclamos(ComparadorDeReclamosABC):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()  # Para vectorizar textos
        self.stop_words = set(stopwords.words('spanish'))  # Palabras comunes en español
        self.stemmer = SnowballStemmer('spanish')  # Stemming para español

    def preprocesar_texto(self, texto: str) -> str:
        """
        Limpia y normaliza el texto: minúsculas, quita puntuación, stemming.
        """
        texto = texto.lower()
        texto = texto.translate(str.maketrans('', '', string.punctuation))  # Quita puntuación
        palabras = nltk.word_tokenize(texto)
        palabras = [self.stemmer.stem(p) for p in palabras if p not in self.stop_words]
        return ' '.join(palabras)

    def encontrar_reclamos_similares(self, nuevo_contenido: str, reclamos_existentes: List[ReclamoDominio], umbral: float = 0.7, top_n: int = 5) :
        """
        Compara un nuevo contenido con reclamos existentes y devuelve los más similares.
        :param nuevo_contenido: Contenido del nuevo reclamo.
        :param reclamos_existentes: Lista de ReclamoDominio existentes.
        :param umbral: Similitud mínima para considerar "parecido".
        :param top_n: Máximo de reclamos similares a devolver.
        :return: Lista de tuplas (reclamo, score_similitud) ordenados por score descendente.
        """
        if not reclamos_existentes:
            return []

        # Preprocesar todos los textos
        contenidos_existentes = [self.preprocesar_texto(r.contenido) for r in reclamos_existentes]
        nuevo_preprocesado = self.preprocesar_texto(nuevo_contenido)

        # Vectorizar
        todos_contenidos = contenidos_existentes + [nuevo_preprocesado]
        tfidf_matrix = self.vectorizer.fit_transform(todos_contenidos)

        # Calcular similitud coseno entre el nuevo (último) y los existentes
        similitudes = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

        # Filtrar por umbral y ordenar
        similares = [reclamos_existentes[i]for i in range(len(similitudes)) if similitudes[i] >= umbral]
        similares.sort(key=lambda x: x.id, reverse=True)  # Orden descendente por ID
        return similares[:top_n]

if __name__ == "__main__":
    # Ejemplo de uso
    reclamos = [
        ReclamoDominio(id=1, usuario_id=1, contenido="El aula 101 tiene problemas con el proyector.", timestamp=None, estado=None, departamento_id=1),
        ReclamoDominio(id=2, usuario_id=2, contenido="Falta material en el laboratorio de computación.", timestamp=None, estado=None, departamento_id=2),
        ReclamoDominio(id=3, usuario_id=3, contenido="El aire acondicionado no funciona en la sala de reuniones.", timestamp=None, estado=None, departamento_id=1),
    ]

    comparador = ComparadorDeReclamos()
    nuevo_reclamo = "El proyector del aula 101 no enciende."
    similares = comparador.encontrar_reclamos_similares(nuevo_reclamo, reclamos, umbral=0.2)

    print("Reclamos similares encontrados:")
    for reclamo in similares:
        print(f"ID: {reclamo.id}, Contenido: {reclamo.contenido}")