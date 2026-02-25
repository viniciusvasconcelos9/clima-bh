import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def MediasDiariasComponent(df,anos_disponiveis):
    st.subheader("📅 Médias Diárias por Mês")

    ano_unico = st.selectbox("Selecione um ano para análise detalhada diária", anos_disponiveis)
    df_ano = df[df['Ano'] == ano_unico]

    meses_disponiveis = sorted(df_ano['Mes'].dropna().unique())
    meses_nomes = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    meses_labels = [meses_nomes[m] for m in meses_disponiveis]
    mes_label = st.selectbox("Selecione o mês", meses_labels)
    meses_selecionados = [k for k, v in meses_nomes.items() if v == mes_label]


    df_diario = df_ano[df_ano['Mes'].isin(meses_selecionados)].groupby(['Mes', 'Dia']).agg({
        "Temp. Ins. (C)": "mean",
        "Umi. Ins. (%)": "mean",
        "Radiacao (KJ/m²)": "mean",
        "Chuva (mm)": "sum"
    }).reset_index()

    df_diario.columns = ['Mês', 'Dia', 'Temperatura', 'Umidade', 'Radiação', 'Chuva']

    def plot_diario(df, y, ylabel, title, color):
        fig, ax = plt.subplots(figsize=(8, 4))
        mes = df['Mês'].iloc[0]
        dados_mes = df[df['Mês'] == mes]
        ax.plot(dados_mes['Dia'], dados_mes[y], label=meses_nomes[mes], color=color)
        ax.set_xlabel("Dia do Mês")
        ax.set_ylabel(ylabel)
        ax.set_title(f"{title} - {meses_nomes[mes]} de {ano_unico}")
        ax.grid(True)
        ax.legend()
        plt.tight_layout()
        return fig

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌡️ Temperatura Média Diária")
        st.pyplot(plot_diario(df_diario, 'Temperatura', '°C', 'Temperatura Média Diária', 'red'))
    with col2:
        st.subheader("☀️ Radiação Média Diária")
        st.pyplot(plot_diario(df_diario, 'Radiação', 'KJ/m²', 'Radiação Média Diária', 'orange'))

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("💧 Umidade Média Diária")
        st.pyplot(plot_diario(df_diario, 'Umidade', '%', 'Umidade Média Diária', 'blue'))
    with col4:
        st.subheader("🌧️ Precipitação Diária")
        st.pyplot(plot_diario(df_diario, 'Chuva', 'mm', 'Precipitação Diária', 'green'))

