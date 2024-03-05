from pathlib import Path
import streamlit as st
import pandas as pd

# ---- PAGE CONFIG ----
st.set_page_config(page_title='Central de Emails',
                   page_icon=':incoming_envelope:',
                   layout='centered')
# https://www.webfx.com/tools/emoji-cheat-sheet/

# ---- HIDE STREAMLIT STYLE ----
def style():
    hide_st_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                        </style>
                    """
    return st.markdown(hide_st_style, unsafe_allow_html=True)

# Load data
def leitura_de_dados():
    if not 'dados' in st.session_state:
        pasta_datasets = Path(__file__).parents[0] / 'datasets'

        df_vendas = pd.read_csv(pasta_datasets / 'vendas.csv', decimal=',', sep=';', index_col=0, parse_dates=True)
        df_filiais = pd.read_csv(pasta_datasets / 'filiais.csv', decimal=',', sep=';', index_col=0)
        df_produtos = pd.read_csv(pasta_datasets / 'produtos.csv', decimal=',', sep=';', index_col=0)

        dados = {'df_vendas': df_vendas,
                'df_filiais': df_filiais,
                'df_produtos': df_produtos}
        st.session_state['caminho_datasets'] = pasta_datasets
        st.session_state['dados'] = dados