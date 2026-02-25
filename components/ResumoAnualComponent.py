import streamlit as st
import pandas as pd


def ResumoAnualComponent(df):
    st.subheader("📅 Resumo de Extremos por Ano")

    # ---------------- VALIDAR DADOS ----------------
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

    df_valid['Data_hora_sp'] = pd.to_datetime(
        df_valid['Data_hora_sp'],
        errors='coerce'
    )

    df_valid = df_valid.sort_values('Data_hora_sp')
    df_valid['Ano'] = df_valid['Data_hora_sp'].dt.year

    # ---------------- SELEÇÃO DE ANO ----------------
    anos_disponiveis = sorted(
        df_valid['Ano'].dropna().unique(),
        reverse=True
    )

    if len(anos_disponiveis) == 0:
        st.warning("Nenhum dado disponível.")
        return

    ano_selecionado = st.selectbox(
        "Selecione o ano",
        anos_disponiveis
    )

    df_ano = df_valid[df_valid['Ano'] == ano_selecionado].copy()

    if df_ano.empty:
        st.warning("Nenhum dado disponível para o ano selecionado.")
        return

    df_ano.set_index('Data_hora_sp', inplace=True)

    # ---------------- EXTREMOS ----------------

    temp_min_idx = df_ano['Temp. Min. (C)'].idxmin()
    temp_min = float(df_ano.loc[temp_min_idx, 'Temp. Min. (C)'])

    temp_max_idx = df_ano['Temp. Max. (C)'].idxmax()
    temp_max = float(df_ano.loc[temp_max_idx, 'Temp. Max. (C)'])

    chuva_max_idx = df_ano['Chuva (mm)'].idxmax()
    chuva_max = float(df_ano.loc[chuva_max_idx, 'Chuva (mm)'])

    rad_max_idx = df_ano['Radiacao (KJ/m²)'].idxmax()
    rad_max = float(df_ano.loc[rad_max_idx, 'Radiacao (KJ/m²)'])

    # ---------------- ACUMULADOS MÓVEIS ----------------

    # 24h móvel
    rolling_24h = df_ano['Chuva (mm)'].rolling('24h').sum()
    chuva_24h_val = rolling_24h.max()
    chuva_24h_idx = rolling_24h.idxmax()

    if pd.notna(chuva_24h_val):
        chuva_24h_val = float(chuva_24h_val)
        chuva_24h_ini = chuva_24h_idx - pd.Timedelta(hours=24)
    else:
        chuva_24h_val = 0.0
        chuva_24h_ini = None

    # 7 dias móvel
    rolling_7d = df_ano['Chuva (mm)'].rolling('168h').sum()
    chuva_7d_val = rolling_7d.max()
    chuva_7d_idx = rolling_7d.idxmax()

    if pd.notna(chuva_7d_val):
        chuva_7d_val = float(chuva_7d_val)
        chuva_7d_ini = chuva_7d_idx - pd.Timedelta(days=7)
    else:
        chuva_7d_val = 0.0
        chuva_7d_ini = None

    # ---------------- CHUVA DIÁRIA (DIA FECHADO) ----------------

    chuva_diaria = df_ano['Chuva (mm)'].resample('D').sum()

    if not chuva_diaria.empty:
        chuva_dia_max = float(chuva_diaria.max())
        chuva_dia_max_data = chuva_diaria.idxmax()
    else:
        chuva_dia_max = 0.0
        chuva_dia_max_data = None

    # ---------------- RADIAÇÃO DIÁRIA (DIA FECHADO) ----------------

    radiacao_diaria = df_ano['Radiacao (KJ/m²)'].resample('D').sum()

    if not radiacao_diaria.empty:
        radiacao_dia_max = float(radiacao_diaria.max())
        radiacao_dia_max_data = radiacao_diaria.idxmax()
    else:
        radiacao_dia_max = 0.0
        radiacao_dia_max_data = None    

    # ---------------- EXIBIÇÃO ----------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🌡️ Temperatura Mínima",
            f"{temp_min:.2f} °C"
        )
        st.write(
            f"📅 {temp_min_idx.strftime('%d/%m/%Y %H:%M')}"
        )

        st.metric(
            "🌧️ Precipitação Máxima",
            f"{chuva_max:.2f} mm"
        )
        st.write(
            f"📅 {chuva_max_idx.strftime('%d/%m/%Y %H:%M')}"
        )

        st.metric(
            "🌧️ Chuva Acumulada (24h)",
            f"{chuva_24h_val:.2f} mm"
        )

        if chuva_24h_ini is not None:
            st.write(
                f"🕒 {chuva_24h_ini.strftime('%d/%m/%Y %H:%M')} - "
                f"{chuva_24h_idx.strftime('%d/%m/%Y %H:%M')}"
            )

        # NOVA MÉTRICA
        st.metric(
            "🌧️ Maior Chuva em um Dia",
            f"{chuva_dia_max:.2f} mm"
        )

        if chuva_dia_max_data is not None:
            st.write(
                f"📅 {chuva_dia_max_data.strftime('%d/%m/%Y')}"
            )

    with col2:
        st.metric(
            "🌡️ Temperatura Máxima",
            f"{temp_max:.2f} °C"
        )
        st.write(
            f"📅 {temp_max_idx.strftime('%d/%m/%Y %H:%M')}"
        )

        st.metric(
            "☀️ Radiação Máxima",
            f"{rad_max:.2f} kJ/m²"
        )
        st.write(
            f"📅 {rad_max_idx.strftime('%d/%m/%Y %H:%M')}"
        )


        st.metric(
            "☀️ Maior Radiação em um Dia",
            f"{radiacao_dia_max:.2f} kJ/m²"
        )

        if radiacao_dia_max_data is not None:
            st.write(
                f"📅 {radiacao_dia_max_data.strftime('%d/%m/%Y')}"
            )

        st.metric(
            "🌧️ Chuva Acumulada (7 dias)",
            f"{chuva_7d_val:.2f} mm"
        )

        if chuva_7d_ini is not None:
            st.write(
                f"🕒 {chuva_7d_ini.strftime('%d/%m/%Y %H:%M')} - "
                f"{chuva_7d_idx.strftime('%d/%m/%Y %H:%M')}"
            )