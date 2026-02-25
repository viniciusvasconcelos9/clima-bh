import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def HeaderComponent():

    st.set_page_config(page_title="Análise Climática", layout="wide")
    st.title("📊 Análise Climática Comparativa")
    st.write("Dados - 2025-2026")
    st.write("Fonte: Instituto Nacional de Meteorologia, INMET - Estação A572")
    st.write("Estação: BELO HORIZONTE - SANTO AGOSTINHO")
    st.write("Localização: -19.9338, -43.9522")
    st.markdown("_Tem algumas inconsistências por falta de dados do ano_")
    st.markdown("*Feito por Vinícius Vasconcelos*")