import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def ResumoComponent(df):
    st.subheader("📋 Resumo Histórico de Extremos Climáticos")

    # Garantir dados válidos
    '''df_valid = df.dropna(subset=[
        'Data_hora_sp',
        'Temp. Max. (C)',
        'Temp. Min. (C)',
        'Chuva (mm)',
        'Radiacao (KJ/m²)'
    ]).copy()'''

    df_valid = df.dropna(subset=[
        'Data_hora_sp',
        'Chuva (mm)'
    ]).copy()

    # Garantir datetime
    df_valid['Data_hora_sp'] = pd.to_datetime(df_valid['Data_hora_sp'])

    # Ordenar e definir índice temporal
    df_valid = df_valid.sort_values('Data_hora_sp')
    df_valid.set_index('Data_hora_sp', inplace=True)

    # ------------------ EXTREMOS ------------------

    temp_min_idx = df_valid['Temp. Min. (C)'].idxmin()
    temp_min = float(df_valid.loc[temp_min_idx, 'Temp. Min. (C)'])

    temp_max_idx = df_valid['Temp. Max. (C)'].idxmax()
    temp_max = float(df_valid.loc[temp_max_idx, 'Temp. Max. (C)'])

    chuva_max_idx = df_valid['Chuva (mm)'].idxmax()
    chuva_max = float(df_valid.loc[chuva_max_idx, 'Chuva (mm)'])

    rad_max_idx = df_valid['Radiacao (KJ/m²)'].idxmax()
    rad_max = float(df_valid.loc[rad_max_idx, 'Radiacao (KJ/m²)'])

    # ------------------ ACUMULADOS ------------------

    # 24h móvel
    rolling_chuva_24h = df_valid['Chuva (mm)'].rolling('24h').sum()
    chuva_24h_idx = rolling_chuva_24h.idxmax()
    chuva_24h_val = float(rolling_chuva_24h.max())
    chuva_24h_fim = chuva_24h_idx
    chuva_24h_ini = chuva_24h_fim - pd.Timedelta(hours=24)

    # 7 dias móvel
    rolling_chuva_7d = df_valid['Chuva (mm)'].rolling('168h').sum()
    chuva_7d_idx = rolling_chuva_7d.idxmax()
    chuva_7d_val = float(rolling_chuva_7d.max())
    chuva_7d_fim = chuva_7d_idx
    chuva_7d_ini = chuva_7d_fim - pd.Timedelta(days=7)

    # ------------------ NOVA MÉTRICA ------------------
    # 🌧️ Maior chuva acumulada dentro do mesmo dia (dia fechado)

    df_valid['Data'] = df_valid.index.date
    chuva_diaria = df_valid.groupby('Data')['Chuva (mm)'].sum()

    chuva_dia_max = float(chuva_diaria.max())
    chuva_dia_max_data = chuva_diaria.idxmax()
# ---------------- RADIAÇÃO DIÁRIA (DIA FECHADO) ----------------

    radiacao_diaria = df_valid['Radiacao (KJ/m²)'].resample('D').sum()

    if not radiacao_diaria.empty:
        radiacao_dia_max = float(radiacao_diaria.max())
        radiacao_dia_max_data = radiacao_diaria.idxmax()
    else:
        radiacao_dia_max = 0.0
        radiacao_dia_max_data = None
    # ------------------ EXIBIÇÃO ------------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🌡️ Temperatura Mínima",
                  f"{temp_min:.2f} °C")
        st.write(f"📅 {temp_min_idx.strftime('%d/%m/%Y %H:%M')}")

        st.metric("🌧️ Precipitação Máxima Pontual",
                  f"{chuva_max:.2f} mm")
        st.write(f"📅 {chuva_max_idx.strftime('%d/%m/%Y %H:%M')}")

        st.metric("🌧️ Chuva Acumulada (24h móvel)",
                  f"{chuva_24h_val:.2f} mm")
        st.write(f"🕒 {chuva_24h_ini.strftime('%d/%m/%Y %H:%M')} - "
                 f"{chuva_24h_fim.strftime('%d/%m/%Y %H:%M')}")

        # 🔥 NOVA MÉTRICA
        st.metric("🌧️ Maior Chuva em um Dia",
                  f"{chuva_dia_max:.2f} mm")
        st.write(f"📅 {pd.to_datetime(chuva_dia_max_data).strftime('%d/%m/%Y')}")

    with col2:
        st.metric("🌡️ Temperatura Máxima",
                  f"{temp_max:.2f} °C")
        st.write(f"📅 {temp_max_idx.strftime('%d/%m/%Y %H:%M')}")

        st.metric("☀️ Radiação Máxima",
                  f"{rad_max:.2f} kJ/m²")
        st.write(f"📅 {rad_max_idx.strftime('%d/%m/%Y %H:%M')}")

        st.metric(
            "☀️ Maior Radiação em um Dia",
            f"{radiacao_dia_max:.2f} kJ/m²"
        )

        if radiacao_dia_max_data is not None:
            st.write(
                f"📅 {radiacao_dia_max_data.strftime('%d/%m/%Y')}"
            )

        st.metric("🌧️ Chuva Acumulada (7 dias móvel)",
                  f"{chuva_7d_val:.2f} mm")
        st.write(f"🕒 {chuva_7d_ini.strftime('%d/%m/%Y %H:%M')} - "
                 f"{chuva_7d_fim.strftime('%d/%m/%Y %H:%M')}")
