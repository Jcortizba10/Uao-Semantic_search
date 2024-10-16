import os
import pandas as pd

class DataLoader:
    @staticmethod
    def load_data(file_path):
        if not os.path.exists(file_path):
            print(f"Archivo no encontrado: {file_path}")
            return None

        try:
            df = pd.read_csv(file_path)
            print("Datos cargados correctamente.")
            return df
        except Exception as e:
            print(f"Error al cargar el archivo: {e.__class__.__name__} - {e}")
            return None
