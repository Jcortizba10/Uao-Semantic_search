import pandas as pd
import warnings
from sentence_transformers import SentenceTransformer, util

warnings.filterwarnings("ignore", category=FutureWarning)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def main(query):
    df = pd.read_csv('./archive/IMDB top 1000.csv')
    df = df.drop_duplicates(subset=['Description'], keep='first')
    descriptions = df['Description'].tolist()
    embeddings = model.encode(descriptions, batch_size=64, show_progress_bar=True)
    df['embeddings'] = embeddings.tolist()
    matching_titles = df[df['Title'].str.contains(query, case=False)]

    if not matching_titles.empty:
        print("Películas encontradas con el título:")
        print(matching_titles[['Title', 'Description']])
    else:
        print("No se encontraron coincidencias exactas en títulos. Buscando por descripciones...")
        query_embedding = model.encode([query])[0]
        df['similarity'] = df.apply(lambda x: compute_similarity(x, query_embedding), axis=1)
        df = df.sort_values(by='similarity', ascending=False)
        print("Películas más similares a tu búsqueda:")
        print(df[['Title', 'Description', 'similarity']].head())
        print("\n--- Fin de la búsqueda ---\n")

def compute_similarity(example, query_embedding):
    embedding = example['embeddings'] 
    similarity = util.cos_sim(embedding, query_embedding).item()
    return similarity  

if __name__ == '__main__':
    while True:
        query = input('Ingresa el término de búsqueda (o escribe "salir" para terminar): ')
        
        if query.lower() == "salir":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        
        main(query)
        continuar = input("\n¿Quieres realizar otra búsqueda? (si/no): ").strip().lower()
        if continuar != "si":
            print("Saliendo del programa. ¡Hasta luego!")
            break