
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configurações Google Sheets
SHEET_ID = "1BI-mFeMh-DELi0ikBgNvNH1HUQ9vPm7j-zZz9ewpv34"
WORKSHEET_NAME = "Utilizadores"

@st.cache_resource
def connect_to_gsheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(credentials)
    return client

def carregar_utilizadores():
    client = connect_to_gsheet()
    sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def login():
    st.title("🔐 Lendismart Login")

    if "login_success" not in st.session_state:
        st.session_state.login_success = False

    with st.form("login_form"):
        email = st.text_input("Email").strip().lower()
        senha = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            df = carregar_utilizadores()
            user = df[(df["Email"].str.lower() == email) & (df["Senha"] == senha)]

            if not user.empty:
                st.session_state.login_success = True
                st.session_state.user_email = email
                st.session_state.user_nome = user.iloc[0]["Nome completo"]
                st.session_state.user_perfil = user.iloc[0]["Perfil"]
                st.success(f"Bem-vindo, {st.session_state['user_nome']} 👋")
            else:
                st.error("Credenciais inválidas. Tenta novamente.")

def logout():
    st.session_state.login_success = False
    for key in ["user_email", "user_nome", "user_perfil"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Sessão terminada com sucesso.")
