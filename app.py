import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from components.ResumoComponent import ResumoComponent
from components.ResumoAnualComponent import ResumoAnualComponent
from components.ComparativoAnualComponent import ComparativoAnualComponent
from components.MediasMensaisComponent import MediasMensaisComponent
from components.MediasDiariasComponent import MediasDiariasComponent
from components.ResumoMensalComponent import ResumoMensalComponent
from layout.HeaderComponent import HeaderComponent

HeaderComponent()

@st.cache_data
def load_data():
    df = pd.read_csv(
        "bh.csv",
        sep=",",
        encoding="utf-8"
    )

    # Conversão explícita garantindo datetime válido
    df["Data_hora_sp"] = pd.to_datetime(
        df["Data_hora_sp"],
        utc=True
    ).dt.tz_convert("America/Sao_Paulo")

    df["Ano"] = df["Data_hora_sp"].dt.year
    df["Mes"] = df["Data_hora_sp"].dt.month
    df["Dia"] = df["Data_hora_sp"].dt.day

    return df


df = load_data()
anos_disponiveis = sorted(df["Ano"].dropna().unique())

aba = st.tabs([
    "📋 Resumo Histórico de Extremos Climáticos",
    "📅 Resumo de Extremos por Ano",
    "📆 Resumo de Extremos por Mês",
    "📈 Comparação entre Anos",
    "📅 Médias Diárias por Mês (Ano único)",
    "📅 Médias Diárias por Mês"
])

# ------------------------ ABA 0 ------------------------
with aba[0]:
    ResumoComponent(df)

# ------------------------ ABA 1 ------------------------
with aba[1]:
    ResumoAnualComponent(df)

# ------------------------ ABA 2 ------------------------
with aba[2]:
    ResumoMensalComponent(df)

# ------------------------ ABA 3 ------------------------
with aba[3]:
    ComparativoAnualComponent(df, anos_disponiveis)

# ------------------------ ABA 4 ------------------------
with aba[4]:
    MediasMensaisComponent(df, anos_disponiveis)

# ------------------------ ABA 5 ------------------------
with aba[5]:
    MediasDiariasComponent(df, anos_disponiveis)