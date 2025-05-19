
import streamlit as st
from modules import simulador, proposta_titular1, proposta_titular2, proposta_avalista, empresa_dados, proposta, bem

st.set_page_config(page_title="Lendismart", layout="wide")

st.sidebar.title("📁 Menu Proposta")

menu = st.sidebar.radio("Navegação", [
    "📊 Simulador",
    "👤 Cliente - 1º Titular",
    "👥 Cliente - 2º Titular",
    "🧾 Cliente - Avalista",
    "🏢 Cliente - Empresa",
    "🚗 Viatura",
    "📄 Proposta resumo"
])

if menu == "📊 Simulador":
    simulador.simulador()

elif menu == "👤 Cliente - 1º Titular":
    proposta_titular1.proposta_titular1()

elif menu == "👥 Cliente - 2º Titular":
    proposta_titular2.proposta_titular2()

elif menu == "🧾 Cliente - Avalista":
    proposta_avalista.proposta_avalista()

elif menu == "🏢 Cliente - Empresa":
    empresa_dados.empresa_dados()

elif menu == "🚗 Viatura":
    bem.bem()

elif menu == "📄 Proposta resumo":
    proposta.proposta()
