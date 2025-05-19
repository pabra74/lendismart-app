import streamlit as st
from datetime import date
import pandas as pd

def carregar_clientes():
    return pd.DataFrame({
        "NIF": ["123456789", "987654321", "654987321"],
        "Nome": ["Paulo Abrantes", "Joana Sousa", "Carlos Silva"]
    })

def proposta():
    st.title("📄 Proposta Resumo")

    df_clientes = carregar_clientes()
    lista_nomes = df_clientes["Nome"].tolist()
    financeiras = ["Credibom", "Cetelem", "321 Crédito", "Cofidis", "Primus", "Montepio", "BBVA", "CA Bank"]

    with st.form("form_proposta"):

        st.subheader("👥 Intervenientes")
        col1, col2, col3 = st.columns(3)
        with col1:
            titular1 = st.selectbox("1º Titular", lista_nomes, key="titular1")
        with col2:
            titular2 = st.selectbox("2º Titular (se aplicável)", ["", "José Costa", "Maria Leal"], key="titular2")
        with col3:
            avalista = st.selectbox("Avalista (se aplicável)", ["", "Carlos Silva", "Ana Matos"], key="avalista")

        empresa = st.selectbox("Empresa (se aplicável)", ["", "BIZAN CONSTRUÇÕES, UNIPESSOAL LDA"], key="empresa")

        st.subheader("📌 Identificador da Proposta")
        if titular1:
            nif = df_clientes[df_clientes["Nome"] == titular1]["NIF"].values[0]
            primeiro_nome = titular1.split()[0]
            hoje = date.today().strftime("%d%m%Y")
            identificador = f"{nif}_{primeiro_nome}_{hoje}"
            st.text_input("Identificador Interno", value=identificador, disabled=True, key="identificador")

        st.subheader("🏦 IBAN")
        iban = st.text_input("IBAN", placeholder="PT50XXXXXXXXXXXXXXX", key="iban")

        st.subheader("🏢 Stand e Simulação")
        col4, col5 = st.columns(2)
        with col4:
            stand = st.selectbox("Stand", ["Rimamundo", "Auto Leandro"], key="stand")
        with col5:
            simulacao = st.selectbox("Simulação (por data)", ["Simulação 2025-05-18", "Simulação 2025-04-10"], key="simulacao")

        st.markdown("### 🔄 Dados da Simulação (preenchidos)")
        st.text_input("Data Matrícula", value="2025/05/18", key="simul_data")
        st.text_input("Categoria", value="Ligeiros de passageiros", key="simul_categoria")
        col6, col7, col8 = st.columns(3)
        with col6:
            st.text_input("Valor PVP (€)", value="0.00", key="simul_pvp")
        with col7:
            st.text_input("Valor Entrada (€)", value="0.00", key="simul_entrada")
        with col8:
            st.text_input("Valor Subvenção (€)", value="0.00", key="simul_subvencao")

        st.markdown("### 💸 Valor a Financiar")
        st.text_input("Valor a Financiar (€)", value="0.00", disabled=True, key="simul_financiado")

        st.markdown("### 🚗 Dados da Viatura (preenchidos)")
        st.text_input("Data da 1ª Matrícula", value="2025/05/18", key="viat_data")
        st.text_input("Categoria", value="Ligeiros de passageiros", key="viat_categoria")
        col9, col10 = st.columns(2)
        with col9:
            st.text_input("Matrícula", key="viat_matricula")
        with col10:
            st.text_input("Nº Chassis", key="viat_chassis")

        col11, col12, col13 = st.columns(3)
        with col11:
            st.text_input("Marca", key="viat_marca")
        with col12:
            st.text_input("Modelo", key="viat_modelo")
        with col13:
            st.text_input("Versão", key="viat_versao")

        st.subheader("🏛️ Financeiras")
        for financeira in financeiras:
            st.markdown(f"**{financeira}**")
            colf1, colf2, colf3 = st.columns(3)
            with colf1:
                st.text_input(f"Nº Proposta {financeira}", key=f"{financeira}_num")
            with colf2:
                st.date_input(f"Data {financeira}", key=f"{financeira}_data")
            with colf3:
                st.selectbox(f"Decisão {financeira}", ["Aguarda", "Aprovada", "Recusada", "Reanálise", "Arquivada", "Financiada"], key=f"{financeira}_decisao")
            st.text_area(f"Observações {financeira}", key=f"{financeira}_obs")

        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.form_submit_button("💾 Gravar")
        with col_btn2:
            st.form_submit_button("✏️ Editar")

    # Botões fora do formulário
    st.markdown("### 📤 Exportações")
    st.button("📥 Exportar Proposta", key="export_geral")
    for financeira in financeiras:
        st.button(f"📤 Exportar dados {financeira}", key=f"export_{financeira}_btn")