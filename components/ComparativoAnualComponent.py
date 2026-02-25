import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def ComparativoAnualComponent(df,anos_disponiveis):
    st.subheader("📆 Comparação entre Anos")

    anos_selecionados = st.multiselect("Selecione os anos para comparar", anos_disponiveis, default=anos_disponiveis[:2])
    df_filtrado = df[df['Ano'].isin(anos_selecionados)]

    df_grouped = df_filtrado.groupby(['Ano', 'Mes']).agg({
        "Temp. Ins. (C)": "mean",
        "Umi. Ins. (%)": "mean",
        "Radiacao (KJ/m²)": "mean",
        "Chuva (mm)": "sum"
    }).reset_index()

    df_grouped.columns = ['Ano', 'Mês', 'Temperatura', 'Umidade', 'Radiação', 'Chuva']

    def gerar_mapa_cores(anos):
        cmap = cm.get_cmap('tab10', len(anos)) if len(anos) <= 10 else cm.get_cmap('hsv', len(anos))
        return {ano: cmap(i) for i, ano in enumerate(anos)}

    def plot_line_chart(df, y, ylabel, title, color_map):
        fig, ax = plt.subplots(figsize=(7, 4))
        for ano in sorted(color_map.keys()):
            dados_ano = df[df['Ano'] == ano]
            ax.plot(dados_ano['Mês'], dados_ano[y], marker='o', label=str(ano), color=color_map[ano])
        ax.set_xlabel("Mês")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True)
        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), title="Ano")
        plt.tight_layout()
        return fig

    color_map = gerar_mapa_cores(anos_selecionados)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌡️ Temperatura Média")
        st.pyplot(plot_line_chart(df_grouped, 'Temperatura', '°C', 'Temperatura Média por Mês', color_map))
    with col2:
        st.subheader("☀️ Radiação Média")
        st.pyplot(plot_line_chart(df_grouped, 'Radiação', 'kJ/m²', 'Radiação Média por Mês', color_map))

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("💧 Umidade Média")
        st.pyplot(plot_line_chart(df_grouped, 'Umidade', '%', 'Umidade Média por Mês', color_map))
    with col4:
        st.subheader("🌧️ Precipitação Total")
        st.pyplot(plot_line_chart(df_grouped, 'Chuva', 'mm', 'Precipitação Total por Mês', color_map))