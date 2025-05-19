
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime

@st.cache_resource
def connect_to_sheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(credentials)
    return client

def gravar_simulador(sheet_id, dados):
    client = connect_to_sheets()
    sheet = client.open_by_key(sheet_id)
    aba = sheet.worksheet("Simulador")

    # Adicionar timestamp
    dados["Data Gravação"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Obter ou criar cabeçalho
    headers = aba.row_values(1)
    if not headers:
        aba.append_row(list(dados.keys()))
        headers = list(dados.keys())

    row = [dados.get(col, "") for col in headers]
    aba.append_row(row)
