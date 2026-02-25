import pandas as pd

dados = pd.read_csv(
    "arquivo_unificado.csv",
    sep=";",
    decimal=","
)


# normaliza nomes das colunas
#dados.columns = dados.columns.str.strip().str.lower()

# cria datetime em UTC
dados["Data_hora"] = pd.to_datetime(
    dados["Data"] + " " + dados["Hora (UTC)"].astype(str).str.zfill(4),
    format="%d/%m/%Y %H%M",
    errors="coerce",
    utc=True
)

# converte para São Paulo
dados["Data_hora_sp"] = dados["Data_hora"].dt.tz_convert("America/Sao_Paulo")

# remove colunas antigas
dados = dados.drop(columns=["Data", "Hora (UTC)", "Data_hora"])

print(dados.head())


dados.to_csv("timoteo-2026-tratado.csv", index=False)

