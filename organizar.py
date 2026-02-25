import pandas as pd

arquivo_entrada = "timoteo-2026-tratado.csv"
arquivo_saida = "bh.csv"
coluna_data = "Data_hora_sp"

print("Lendo arquivo...")
df = pd.read_csv(arquivo_entrada)

print("Convertendo coluna de data/hora (mantendo timezone original)...")
df[coluna_data] = pd.to_datetime(df[coluna_data])

print("Ordenando dados...")
df = df.sort_values(by=coluna_data)

print("Salvando arquivo ordenado...")
df.to_csv(arquivo_saida, index=False)

print("Processo concluído!")