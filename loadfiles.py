import pandas as pd

class LoadFiles:

    def __init__(self, path, files):
        self.files = files
        self.path = path

    def load_all_files(self):
        # Criar uma lista para armazenar os DataFrames
        dataframes = []
        # Iterar sobre os arquivos e carregar cada um
        for arquivo in self.files:
            print(f'{self.path}/{arquivo}')
            df = self.carregar_arquivo_csv(f'{self.path}/{arquivo}')
            if df is not None:
                dataframes.append(df)

        # Concatenar todos os DataFrames em um único DataFrame
        if dataframes:
            df_combinado = pd.concat(dataframes, ignore_index=True)
            return df_combinado
        else:
            return None

    def carregar_arquivo_csv(self, caminho_arquivo):
        try:
            df = pd.read_csv(caminho_arquivo, encoding="ISO-8859-1", sep=';')
            print(f"Arquivo CSV carregado com sucesso: {caminho_arquivo}")
            return df
        except Exception as e:
            print(f"Erro ao carregar o arquivo CSV: {e}")
            return None