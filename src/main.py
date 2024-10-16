from data_loader import DataLoader
from embedding_search import EmbeddingSearch
from movie_search import MovieSearchApp

if __name__ == '__main__':
    data_loader = DataLoader()
    search_engine = EmbeddingSearch()
    app = MovieSearchApp(data_loader, search_engine)
    
    app.run()
