import pandas as pd
from sentence_transformers import SentenceTransformer, util

class SimilaritySearchInterface:
    def create_embeddings(self, df, context_columns):
        raise NotImplementedError

    def compare_similarity(self, example, query_embedding):
        raise NotImplementedError

    def search(self, df, query, top_n, context_columns):
        raise NotImplementedError

class EmbeddingSearch(SimilaritySearchInterface):
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def create_embeddings(self, df, context_columns):
        # Asegúrate de que los context_columns son los correctos
        if df.empty:
            raise ValueError("El DataFrame está vacío. Debe contener datos para generar embeddings.")

        # Obtener el texto de las columnas contextuales
        texts = df[context_columns].apply(lambda x: ' '.join(x), axis=1).tolist()
        
        # Generar embeddings utilizando el modelo
        embeddings = self.model.encode(texts, convert_to_tensor=True)  # Asegúrate de usar el modelo correcto

        # Convertir a una lista si es necesario
        embeddings = embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings

        # Agregar los embeddings al DataFrame
        df['embeddings'] = embeddings
        
        return df


    def compare_similarity(self, example, query_embedding):
        try:
            embedding = example['embeddings']
            similarity = util.cos_sim(embedding, query_embedding).item()
            return similarity
        except Exception as e:
            print(f"Error al calcular similitud: {e}")
            return 0.0

    def search(self, df, query, top_n=5, context_columns=['Description']):
        query_embedding = self.model.encode([query])[0]
        df = self.create_embeddings(df, context_columns)
        
        df['similarity'] = df.apply(lambda x: self.compare_similarity(x, query_embedding), axis=1)
        df = df.drop_duplicates(subset=['Title'])
        df = df.sort_values(by='similarity', ascending=False)
        return df.head(top_n)
