
import streamlit as st
from datetime import date
from fpdf import FPDF  # fpdf2

def gerar_pdf_empresa(nome, checklist):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Documentos em falta – Empresa: {nome}", ln=True, align="L")
    pdf.ln(5)
    for doc in checklist:
        if doc["Estado"] == "FALTA":
            linha = f"{doc['Documento']}: FALTA – {doc['Observacoes']}"
            pdf.set_text_color(255, 0, 0)
            pdf.cell(200, 10, linha, ln=True, align="L")
    file_path = f"/mnt/data/documentos_faltam_empresa_{nome.replace(' ', '_')}.pdf"
    pdf.output(file_path)
    return file_path

def empresa_dados():
    st.title("👔 Empresa – Dados")

    with st.form("form_empresa"):

        st.subheader("📇 Identificação da Empresa")
        col1, col2 = st.columns(2)
        with col1:
            nome_empresa = st.text_input("Nome da Empresa")
            contato = st.text_input("Contato Telefónico", max_chars=9)
        with col2:
            nipc = st.text_input("NIPC", max_chars=9)
            email = st.text_input("Email")

        st.subheader("📌 Dados Operacionais")
        fornecedores = ["Rimamundo", "Auto Leandro", "Stand Exemplo"]
        fornecedor = st.selectbox("Fornecedor", fornecedores)

        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            certidao_com = st.text_input("Código Certidão Comercial (####-####-####)", placeholder="2825-2885-5475")
        with col_a2:
            rcbe = st.text_input("Código RCBE (8-4-4-12)", placeholder="936c9921-498f-4f88-9df5-c50d264e2fa0")
        with col_a3:
            iban = st.text_input("IBAN (PT50 + 21 dígitos)", placeholder="PT50XXXXXXXXXXXXXXX")

        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            morada = st.text_input("Morada")
        with col_b2:
            porta = st.text_input("Porta")
        with col_b3:
            andar = st.text_input("Andar")

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            codigo_postal = st.text_input("Código Postal", placeholder="0000-000")
        with col_c2:
            localidade = st.text_input("Localidade")

        st.subheader("📎 Checklist Documental (Empresa)")
        docs_empresa = [
            "Cartão de Identificação de Pessoa Coletiva",
            "Código de acesso à Certidão Permanente",
            "Último balancete e certidões de não dívida",
            "Último IRC",
            "Último IES",
            "Último RCBE",
            "Comprovativo de IBAN",
            "Comprovativo de morada empresa",
            "Sócios CC",
            "Sócios Comprovativo morada"
        ]

        checklist = []
        for doc in docs_empresa:
            col1, col2 = st.columns([1, 2])
            with col1:
                estado = st.selectbox(f"{doc}", ["OK", "FALTA"], key=doc)
            with col2:
                obs = st.text_input(f"Observações {doc}", key=doc + "_obs")
            checklist.append({"Documento": doc, "Estado": estado, "Observacoes": obs})

        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            gravar = st.form_submit_button("💾 Gravar")
        with col_btn2:
            editar = st.form_submit_button("✏️ Alterar / Modificar")
        with col_btn3:
            gerar_pdf = st.form_submit_button("🧾 Exportar PDF Documentos em Falta")

        if gerar_pdf and nome_empresa:
            caminho_pdf = gerar_pdf_empresa(nome_empresa, checklist)
            st.success("PDF gerado com sucesso.")
            st.markdown(f"[📄 Abrir PDF]({caminho_pdf})")
