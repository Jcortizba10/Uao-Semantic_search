from embedding_search import EmbeddingSearch
from data_loader import DataLoader

class MovieSearchApp:
    def __init__(self, data_loader: DataLoader, search_engine: EmbeddingSearch):
        self.data_loader = data_loader
        self.search_engine = search_engine

    def run(self):
        while True:
            query = input('Ingresa el término de búsqueda (o escribe "salir" para terminar): ')
            
            if query.lower() == "salir":
                print("Saliendo del programa. ¡Hasta luego!")
                break
            
            self.main(query)

            continuar = input("\n¿Quieres realizar otra búsqueda? (si/no): ").strip().lower()
            if continuar != "si":
                print("Saliendo del programa. ¡Hasta luego!")
                break

    def main(self, query):
        file_path = './src/archive/IMDB_top_1000.csv'
        df = self.data_loader.load_data(file_path)
        
        if df is None:
            print("No se pudo cargar el archivo. Verifica la ruta y el formato del archivo CSV.")
            return
        
        matching_titles = df[df['Title'].str.contains(query, case=False, na=False)]
        
        if not matching_titles.empty:
            print("Películas encontradas con el título:")
            matching_titles = matching_titles.drop_duplicates(subset=['Title'])
            print(matching_titles[['Title', 'Description']])
        else:
            print("No se encontraron coincidencias exactas en títulos. Buscando por descripciones...")
            results = self.search_engine.search(df, query, top_n=5, context_columns=['Title', 'Description'])
            print("Películas más similares a tu búsqueda:")
            print(results[['Title', 'Description', 'similarity']])
