from loadfiles import LoadFiles
import unidecode
import pandas as pd

files = ['bem_candidato_2024_AP.csv', 'bem_candidato_2024_GO.csv', 'bem_candidato_2024_RR.csv']

load_files = LoadFiles('files', files)
df = load_files.load_all_files()

# print(df.head())

# Remove acentos de todas as colunas do DataFrame
for coluna in df.columns:
    if df[coluna].dtype == 'object':
        df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)
        df[coluna] = df[coluna].apply(lambda x: str(x).replace("'", "") if pd.notnull(x) else x)
print("Acentos removidos com sucesso de todas as colunas do DataFrame.")

# Converte VR_BEM_CANDIDATO para valor double
df['VR_BEM_CANDIDATO'] = df['VR_BEM_CANDIDATO'].str.replace(',', '.').astype(float)
print("Coluna VR_BEM_CANDIDATO convertida para valor double com sucesso.")

columns = ['SQ_CANDIDATO', 'DS_BEM_CANDIDATO', 'VR_BEM_CANDIDATO']
df_bem_candidato = df[columns]

# Gera um arquivo SQL no formato INSERT INTO bem_candidato (SQ_CANDIDATO, DS_BEM_CANDIDATO, VR_BEM_CANDIDATO) VALUES ...
# Gera o arquivo SQL
with open('insert_bem_candidato.sql', 'w', encoding='utf-8') as f:
    for _, row in df_bem_candidato.iterrows():
        valores = [f"'{str(row[col]).replace("'", "''")}'" if col != 'VR_BEM_CANDIDATO' else str(row[col]) for col in columns]
        valores_str = ', '.join(valores)
        f.write(f"INSERT INTO bem_candidato (SQ_CANDIDATO, DS_BEM_CANDIDATO, VR_BEM_CANDIDATO) VALUES ({valores_str});\n")
print("Arquivo SQL 'insert_bem_candidato.sql' gerado com sucesso.")


