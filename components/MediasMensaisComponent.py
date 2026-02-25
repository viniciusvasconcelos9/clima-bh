import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def MediasMensaisComponent(df,anos_disponiveis):
    st.subheader("📆 Análise de um Ano com Variação Mensal")

    ano_selecionado = st.selectbox("Selecione um ano", anos_disponiveis)
    df_ano = df[df['Ano'] == ano_selecionado]

    df_mensal = df_ano.groupby('Mes').agg({
        "Temp. Ins. (C)": ['mean', 'min', 'max'],
        "Umi. Ins. (%)": ['mean', 'min', 'max'],
        "Radiacao (KJ/m²)": ['mean', 'min', 'max'],
        "Chuva (mm)": ['sum', 'min', 'max']  # Precipitação como total, mas mostra min/max para coerência
    }).reset_index()

    df_mensal.columns = ['Mês',
                         'Temp_Media', 'Temp_Min', 'Temp_Max',
                         'Umi_Media', 'Umi_Min', 'Umi_Max',
                         'Rad_Media', 'Rad_Min', 'Rad_Max',
                         'Chuva_Total', 'Chuva_Min', 'Chuva_Max']

    def plot_barras_com_erro(df, media_col, min_col, max_col, ylabel, title, color):
        fig, ax = plt.subplots(figsize=(7, 4))
        x = df['Mês']
        y = df[media_col]

        # Corrigir para evitar valores negativos nas barras de erro
        yerr_lower = (y - df[min_col]).clip(lower=0)
        yerr_upper = (df[max_col] - y).clip(lower=0)
        yerr = [yerr_lower, yerr_upper]

        ax.bar(x, y, yerr=yerr, capsize=5, color=color, alpha=0.7)
        ax.set_xlabel("Mês")
        ax.set_ylabel(ylabel)
        ax.set_title(title + f" - {ano_selecionado}")
        ax.grid(True, axis='y')
        ax.set_xticks(range(1, 13))
        plt.tight_layout()
        return fig


    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌡️ Temperatura Média (com min/max)")
        st.pyplot(plot_barras_com_erro(df_mensal, 'Temp_Media', 'Temp_Min', 'Temp_Max', '°C', 'Temperatura Média Mensal', 'salmon'))

    with col2:
        st.subheader("☀️ Radiação Média (com min/max)")
        st.pyplot(plot_barras_com_erro(df_mensal, 'Rad_Media', 'Rad_Min', 'Rad_Max', 'KJ/m²', 'Radiação Mensal Média', 'gold'))

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("💧 Umidade Média (com min/max)")
        st.pyplot(plot_barras_com_erro(df_mensal, 'Umi_Media', 'Umi_Min', 'Umi_Max', '%', 'Umidade Média Mensal', 'skyblue'))

    with col4:
        st.subheader("🌧️ Precipitação Total (com min/max)")
        st.pyplot(plot_barras_com_erro(df_mensal, 'Chuva_Total', 'Chuva_Min', 'Chuva_Max', 'mm', 'Precipitação Mensal Total', 'mediumseagreen'))
