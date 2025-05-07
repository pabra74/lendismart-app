
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

def autenticar_google_sheets():
    # Scopes necessários para acesso ao Google Sheets
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    
    # Carregar credenciais do secrets
    credenciais_info = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(credenciais_info, scopes=SCOPES)
    
    # Autorizar com gspread
    cliente = gspread.authorize(credentials)
    return cliente
