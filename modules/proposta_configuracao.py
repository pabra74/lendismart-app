
import streamlit as st
from datetime import date, datetime

def gerar_identificador(nif, nome):
    hoje = datetime.now().strftime("%d%m%Y")
    primeiro_nome = nome.split()[0] if nome else "Nome"
    return f"{nif}_{primeiro_nome}_{hoje}"

def proposta():
    st.title("📄 Proposta")

    st.subheader("🔑 Identificador Interno")
    col1, col2 = st.columns(2)
    with col1:
        nif = st.text_input("NIF do 1º Titular", max_chars=9)
    with col2:
        nome = st.text_input("Nome do 1º Titular")

    if nif and nome:
        identificador = gerar_identificador(nif, nome)
        st.text_input("Identificador da Proposta", value=identificador, disabled=True)

    st.subheader("👥 Intervenientes")
    col3, col4, col5 = st.columns(3)
    with col3:
        titular1 = st.text_input("1º Titular")
    with col4:
        titular2 = st.text_input("2º Titular")
    with col5:
        avalista = st.text_input("Avalista")

    st.subheader("🏦 IBAN")
    iban = st.text_input("IBAN", placeholder="PT50XXXXXXXXXXXXXXXXXXXXX", max_chars=25)

    st.subheader("💼 Financeiras")

    financeiras = ["Credibom", "Cetelem", "321 Crédito", "Cofidis", "Primus", "Montepio", "BBVA", "CA Bank"]
    estados = ["Aguarda", "Aprovada", "Recusada", "Reanálise", "Arquivada", "Financiada"]

    for banco in financeiras:
        st.markdown(f"**{banco}**")
        colf1, colf2, colf3 = st.columns([3, 2, 3])
        with colf1:
            st.text_input(f"Nº proposta {banco}", key=f"num_{banco}")
        with colf2:
            st.date_input("Data", key=f"data_{banco}", value=date.today())
        with colf3:
            st.selectbox("Decisão", estados, key=f"decisao_{banco}")
