import streamlit as st
import pandas as pd


def ResumoMensalComponent(df):
    st.subheader("📆 Resumo de Extremos por Mês")

    # ---------------- VALIDAR DADOS ----------------
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
    df_valid['Mes'] = df_valid['Data_hora_sp'].dt.month

    # ---------------- SELEÇÃO DE ANO ----------------
    anos_disponiveis = sorted(
        df_valid['Ano'].dropna().unique(),
        reverse=True
    )

    if not anos_disponiveis:
        st.warning("Nenhum dado disponível.")
        return

    ano_selecionado = st.selectbox(
        "Selecione o ano",
        anos_disponiveis,
        key="ano_mensal"
    )

    df_ano = df_valid[df_valid['Ano'] == ano_selecionado].copy()

    # ---------------- SELEÇÃO DE MÊS ----------------
    meses_disponiveis = sorted(
        df_ano['Mes'].dropna().unique()
    )

    if not meses_disponiveis:
        st.warning("Nenhum dado disponível para o ano selecionado.")
        return

    # Dicionário fixo para meses em português
    meses_pt = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    mes_selecionado = st.selectbox(
        "Selecione o mês",
        meses_disponiveis,
        format_func=lambda x: meses_pt.get(x, str(x)),
        key="mes_mensal"
    )

    df_mes = df_ano[df_ano['Mes'] == mes_selecionado].copy()

    if df_mes.empty:
        st.warning("Nenhum dado disponível para o mês selecionado.")
        return

    df_mes.set_index('Data_hora_sp', inplace=True)

    # ---------------- EXTREMOS ----------------

    temp_min_idx = df_mes['Temp. Min. (C)'].idxmin()
    temp_min = float(df_mes.loc[temp_min_idx, 'Temp. Min. (C)'])

    temp_max_idx = df_mes['Temp. Max. (C)'].idxmax()
    temp_max = float(df_mes.loc[temp_max_idx, 'Temp. Max. (C)'])

    chuva_max_idx = df_mes['Chuva (mm)'].idxmax()
    chuva_max = float(df_mes.loc[chuva_max_idx, 'Chuva (mm)'])

    rad_max_idx = df_mes['Radiacao (KJ/m²)'].idxmax()
    rad_max = float(df_mes.loc[rad_max_idx, 'Radiacao (KJ/m²)'])

    # ---------------- RADIAÇÃO DIÁRIA ----------------
    rad_diaria = df_mes['Radiacao (KJ/m²)'].resample('D').sum()

    if not rad_diaria.empty:
        rad_dia_max = float(rad_diaria.max())
        rad_dia_max_data = rad_diaria.idxmax()
    else:
        rad_dia_max = 0.0
        rad_dia_max_data = None

    # ---------------- ACUMULADO 24H (24 REGISTROS) ----------------
    rolling_24h = df_mes['Chuva (mm)'].rolling(window=24).sum()
    chuva_24h_val = rolling_24h.max()
    chuva_24h_idx = rolling_24h.idxmax()

    if pd.notna(chuva_24h_val):
        chuva_24h_val = float(chuva_24h_val)
        pos = df_mes.index.get_loc(chuva_24h_idx)
        chuva_24h_ini = df_mes.index[pos - 23]
    else:
        chuva_24h_val = 0.0
        chuva_24h_ini = None

    # ---------------- ACUMULADO 7 DIAS (168 REGISTROS) ----------------
    rolling_7d = df_mes['Chuva (mm)'].rolling(window=168).sum()
    chuva_7d_val = rolling_7d.max()
    chuva_7d_idx = rolling_7d.idxmax()

    if pd.notna(chuva_7d_val):
        chuva_7d_val = float(chuva_7d_val)
        pos7 = df_mes.index.get_loc(chuva_7d_idx)
        chuva_7d_ini = df_mes.index[pos7 - 167]
    else:
        chuva_7d_val = 0.0
        chuva_7d_ini = None

    # ---------------- CHUVA DIÁRIA ----------------
    chuva_diaria = df_mes['Chuva (mm)'].resample('D').sum()

    if not chuva_diaria.empty:
        chuva_dia_max = float(chuva_diaria.max())
        chuva_dia_max_data = chuva_diaria.idxmax()
    else:
        chuva_dia_max = 0.0
        chuva_dia_max_data = None

    # ---------------- EXIBIÇÃO ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.metric("🌡️ Temperatura Mínima", f"{temp_min:.2f} °C")
        st.write(f"📅 {temp_min_idx.strftime('%d/%m/%Y %H:%M')}")

        st.metric("🌧️ Precipitação Máxima", f"{chuva_max:.2f} mm")
        st.write(f"📅 {chuva_max_idx.strftime('%d/%m/%Y %H:%M')}")

        st.metric("🌧️ Chuva Acumulada (24h)", f"{chuva_24h_val:.2f} mm")

        if chuva_24h_ini is not None:
            st.write(
                f"🕒 {chuva_24h_ini.strftime('%d/%m/%Y %H:%M')} - "
                f"{chuva_24h_idx.strftime('%d/%m/%Y %H:%M')}"
            )

        st.metric("🌧️ Maior Chuva em um Dia", f"{chuva_dia_max:.2f} mm")

        if chuva_dia_max_data is not None:
            st.write(f"📅 {chuva_dia_max_data.strftime('%d/%m/%Y')}")

    with col2:
        st.metric("🌡️ Temperatura Máxima", f"{temp_max:.2f} °C")
        st.write(f"📅 {temp_max_idx.strftime('%d/%m/%Y %H:%M')}")

        st.metric("☀️ Radiação Máxima", f"{rad_max:.2f} kJ/m²")
        st.write(f"📅 {rad_max_idx.strftime('%d/%m/%Y %H:%M')}")

        st.metric("☀️ Maior Radiação em um Dia", f"{rad_dia_max:.2f} kJ/m²")

        if rad_dia_max_data is not None:
            st.write(f"📅 {rad_dia_max_data.strftime('%d/%m/%Y')}")

        st.metric("🌧️ Chuva Acumulada (7 dias)", f"{chuva_7d_val:.2f} mm")

        if chuva_7d_ini is not None:
            st.write(
                f"🕒 {chuva_7d_ini.strftime('%d/%m/%Y %H:%M')} - "
                f"{chuva_7d_idx.strftime('%d/%m/%Y %H:%M')}"
            )