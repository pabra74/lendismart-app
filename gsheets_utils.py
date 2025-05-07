
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def autenticar_google_sheets():
    credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
    cliente = gspread.authorize(credentials)
    sheet = cliente.open("LendismartDB")
    return sheet

def gravar_em_sheet(sheet, aba_nome, dados_dict, chave="id"):
    ws = sheet.worksheet(aba_nome)
    headers = ws.row_values(1)
    valores = [str(dados_dict.get(h, "")) for h in headers]

    todas_linhas = ws.get_all_records()
    for i, linha in enumerate(todas_linhas, start=2):
        if str(linha.get(chave, "")).strip() == str(dados_dict.get(chave, "")).strip():
            ws.update(f"A{i}", [valores])
            return "Atualizado"

    ws.append_row(valores)
    return "Gravado"

def carregar_todos_de_sheet(sheet, aba_nome):
    ws = sheet.worksheet(aba_nome)
    return ws.get_all_records()

def obter_colunas(sheet, aba_nome):
    ws = sheet.worksheet(aba_nome)
    return ws.row_values(1)
