from loadfiles import LoadFiles
import unidecode
import pandas as pd

files = ['rede_social_candidato_2024_AP.csv', 'rede_social_candidato_2024_GO.csv', 'rede_social_candidato_2024_RR.csv']

load_files = LoadFiles('files', files)
df = load_files.load_all_files()

# print(df.head())
# Remove acentos de todas as colunas do DataFrame
for coluna in df.columns:
    if df[coluna].dtype == 'object':
        df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)
        df[coluna] = df[coluna].apply(lambda x: str(x).replace("'", "") if pd.notnull(x) else x)
print("Acentos removidos com sucesso de todas as colunas do DataFrame.")

columns = ['SQ_CANDIDATO', 'DS_URL']
df_bem_candidato = df[columns]

# Gera um arquivo SQL no formato INSERT INTO rede_social (SQ_CANDIDATO, DS_URL) VALUES ...
with open('insert_rede_social.sql', 'w', encoding='utf-8') as f:
    for _, row in df_bem_candidato.iterrows():
        valores = ', '.join([f"'{str(row[col]).replace("'", "''")}'" for col in columns])
        f.write(f"INSERT INTO rede_social (SQ_CANDIDATO, DS_URL) VALUES ({valores});\n")
print("Arquivo SQL 'insert_rede_social.sql' gerado com sucesso.")



