
import streamlit as st
from datetime import date

def bem():
    st.title("🚗 Viatura – Dados do Bem")

    with st.form("form_viatura"):
        st.subheader("📆 Caracterização do Bem")
        col1, col2 = st.columns(2)
        with col1:
            data_matricula = st.date_input("Data da 1ª Matrícula", min_value=date(1970, 1, 1), max_value=date.today())
        with col2:
            categoria = st.selectbox("Categoria", [
                "Ligeiros de passageiros", "Comerciais ligeiros", "Tratores agrícolas", 
                "Máquinas industriais", "Motos", "Todo o terreno", "Caravanas"
            ])

        st.subheader("🚘 Dados do Bem")
        col3, col4 = st.columns(2)
        with col3:
            matricula = st.text_input("Matrícula (ex: AA-00-00)")
        with col4:
            chassis = st.text_input("Nº Chassis", max_chars=17)

        col5, col6 = st.columns(2)
        with col5:
            marca = st.text_input("Marca")
        with col6:
            modelo = st.text_input("Modelo")

        versao = st.text_input("Versão")

        col7, col8 = st.columns(2)
        with col7:
            portas = st.number_input("Nº Portas", min_value=1, step=1)
        with col8:
            potencia = st.number_input("Potência (cv)", min_value=1, step=1)

        col9, col10 = st.columns(2)
        with col9:
            peso_bruto = st.number_input("Peso Bruto (kg)", min_value=0, step=1)
        with col10:
            cilindrada = st.number_input("Cilindrada / POT KW", min_value=0, step=1)

        importado = st.selectbox("Veículo Importado?", ["Não", "Sim"])

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            gravar = st.form_submit_button("💾 Gravar")
        with col_btn2:
            editar = st.form_submit_button("✏️ Editar")

        if gravar:
            st.success("✅ Dados gravados com sucesso.")
        if editar:
            st.info("✏️ Modo edição ativado.")
