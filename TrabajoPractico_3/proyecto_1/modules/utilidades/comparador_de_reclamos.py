from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import string
from modules.dominio.reclamo import ReclamoDominio
from abc import ABC, abstractmethod

nlp = spacy.load("es_core_news_sm")

class ComparadorDeReclamosABC(ABC):
    @abstractmethod
    def encontrar_reclamos_similares(self, nuevo_contenido: str, reclamos_existentes: List[ReclamoDominio], umbral: float = 0.7, top_n: int = 5) :
        pass

class ComparadorDeReclamos(ComparadorDeReclamosABC):
    def __init__(self):
        self.__vectorizer = TfidfVectorizer()  # Para vectorizar textos
        self.__stop_words = nlp.Defaults.stop_words  # Stopwords de spaCy
        # No necesitamos un stemmer con spaCy, ya que usaremos lematización

    def preprocesar_texto(self, texto: str) -> str:
        """
        Limpia y normaliza el texto: minúsculas, quita puntuación, lematización.
        """
        texto = texto.lower()  # Convertir a minúsculas
        doc = nlp(texto)  # Procesar el texto con spaCy

        # Lematizar y filtrar las stopwords y signos de puntuación
        palabras = [token.lemma_ for token in doc if token.text not in self.__stop_words and not token.is_punct]

        return ' '.join(palabras)

    def encontrar_reclamos_similares(self, nuevo_contenido: str, reclamos_existentes: List[ReclamoDominio], umbral: float = 0.7, top_n: int = 5):
        """
        Compara un nuevo contenido con reclamos existentes y devuelve los más similares.
        :param nuevo_contenido: Contenido del nuevo reclamo.
        :param reclamos_existentes: Lista de ReclamoDominio existentes.
        :param umbral: Similitud mínima para considerar "parecido".
        :param top_n: Máximo de reclamos similares a devolver.
        :return: Lista de ReclamoDominio ordenados por similitud descendente.
        """
        if not reclamos_existentes:
            return []

        # Preprocesar todos los textos
        contenidos_existentes = [self.preprocesar_texto(r.contenido) for r in reclamos_existentes]
        nuevo_preprocesado = self.preprocesar_texto(nuevo_contenido)

        # Vectorizar
        todos_contenidos = contenidos_existentes + [nuevo_preprocesado]
        tfidf_matrix = self.__vectorizer.fit_transform(todos_contenidos)

        # Calcular similitud coseno entre el nuevo (último) y los existentes
        similitudes = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

        # Filtrar por umbral y ordenar
        similares = [reclamos_existentes[i] for i in range(len(similitudes)) if similitudes[i] >= umbral]

        # Ordenar los reclamos por la similitud en orden descendente
        similares = [reclamos_existentes[i] for i in sorted(range(len(similitudes)), key=lambda i: similitudes[i], reverse=True) if similitudes[i] >= umbral]

        # Limitar a los top_n reclamos más similares
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