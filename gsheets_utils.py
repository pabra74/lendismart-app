
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def autenticar_google_sheets():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    credenciais_info = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(credenciais_info, scopes=SCOPES)
    cliente = gspread.authorize(credentials)
    return cliente

def gravar_em_sheet(sheet, nome_aba, dados: pd.DataFrame):
    try:
        if nome_aba in [ws.title for ws in sheet.worksheets()]:
            aba = sheet.worksheet(nome_aba)
            sheet.del_worksheet(aba)
        nova_aba = sheet.add_worksheet(title=nome_aba, rows=dados.shape[0]+10, cols=dados.shape[1]+10)
        nova_aba.update([dados.columns.values.tolist()] + dados.values.tolist())
    except Exception as e:
        st.error(f"Erro ao gravar na aba '{nome_aba}': {e}")

def carregar_todos_de_sheet(sheet):
    tabelas = {}
    for aba in sheet.worksheets():
        try:
            df = pd.DataFrame(aba.get_all_records())
            tabelas[aba.title] = df
        except Exception as e:
            st.warning(f"Não foi possível carregar a aba {aba.title}: {e}")
    return tabelas

def obter_colunas(sheet, nome_aba):
    try:
        aba = sheet.worksheet(nome_aba)
        df = pd.DataFrame(aba.get_all_records())
        return df.columns.tolist()
    except Exception as e:
        st.error(f"Erro ao obter colunas da aba '{nome_aba}': {e}")
        return []
