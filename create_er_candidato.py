from loadfiles import LoadFiles
import pandas as pd
import unidecode

files = ['consulta_cand_2024_AP.csv', 'consulta_cand_2024_GO.csv', 'consulta_cand_2024_RR.csv']

load_files = LoadFiles('files', files)
df = load_files.load_all_files()

# Remove acentos de todas as colunas do DataFrame
for coluna in df.columns:
    if df[coluna].dtype == 'object':
        df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)
        df[coluna] = df[coluna].apply(lambda x: str(x).replace("'", "") if pd.notnull(x) else x)
print("Acentos removidos com sucesso de todas as colunas do DataFrame.")

print(df.head())
#print(df.info())
columns = [
    'ANO_ELEICAO', 'SG_UF', 'NM_UE', 'DS_CARGO', 'SQ_CANDIDATO', 
    'NR_CANDIDATO', 'NM_URNA_CANDIDATO', 'NR_PARTIDO', 'SG_PARTIDO', 'NM_PARTIDO', 
    'SG_UF_NASCIMENTO', 'DT_NASCIMENTO', 'DS_GENERO', 'DS_GRAU_INSTRUCAO', 'DS_ESTADO_CIVIL', 
    'DS_COR_RACA', 'DS_OCUPACAO']

df_candidato = df[columns]
#print(df_candidato.head())

# Separa as SG_UF e NM_UE e monta um pandas com valores únicos
df_cidades = df[['SG_UF', 'NM_UE']].drop_duplicates()
# Gera um arquivo sql no formato INSERT INTO cidades (id, SG_UF, NM_UE) VALUES (1, "AP", "Amapá")
# Adiciona uma coluna de ID
df_cidades = df_cidades.reset_index(drop=True)
df_cidades['ID_CIDADE'] = df_cidades.index + 1
# Gera o arquivo SQL
with open('insert_cidades.sql', 'w', encoding='utf-8') as f:
    for _, row in df_cidades.iterrows():
        f.write(f"INSERT INTO cidades (id, SG_UF, NM_UE) VALUES ({row['ID_CIDADE']}, '{row['SG_UF']}', '{row['NM_UE']}');\n")
print("Arquivo SQL 'insert_cidades.sql' gerado com sucesso.")

# Adiciona a coluna SQ_CIDADE na variável df_candidato com base na variável df_cidades
df_candidato = df_candidato.merge(df_cidades, on=['SG_UF', 'NM_UE'], how='left')
#print(df_candidato.head())
# Gera um arquivo insert_candidatos.sql de INSERT usando todas as colunas de df_candidato menos SG_UF e NM_UE
# Remove as colunas SG_UF e NM_UE do DataFrame
colunas_para_inserir = [col for col in df_candidato.columns if col not in ['SG_UF', 'NM_UE']]
with open('insert_candidatos.sql', 'w', encoding='utf-8') as f:
    for _, row in df_candidato.iterrows():
        colunas = ', '.join(colunas_para_inserir)
        valores = ', '.join([f"'{str(row[col]).replace("'", "''")}'" for col in colunas_para_inserir])
        f.write(f"INSERT INTO candidatos ({colunas}) VALUES ({valores});\n")
print("Arquivo SQL 'insert_candidatos.sql' gerado com sucesso.")