
import streamlit as st
from datetime import date, datetime
import pandas as pd
from fpdf import FPDF  # fpdf2

def carregar_clientes():
    return pd.DataFrame({
        "NIF": ["123456789", "987654321"],
        "Nome": ["Paulo Abrantes", "Joana Sousa"],
        "Data_Nascimento": ["1980-05-10", "1992-09-15"]
    })

def gerar_identificador(nif, nome):
    hoje = datetime.now().strftime("%d%m%Y")
    primeiro_nome = nome.split()[0] if nome else "Nome"
    return f"{nif}_{primeiro_nome}_{hoje}"

def calcular_vencimentos(duodecimos, rv1, rv2, rv3, sa1, sa2, sa3):
    media_recibos = (rv1 + rv2 + rv3) / 3
    media_subs = (sa1 + sa2 + sa3) / 3
    if duodecimos == "Sim":
        venc_a = media_recibos
    else:
        venc_a = (media_recibos * 14 / 12) + (media_subs * 11 / 12)
    venc_b = (rv1 + sa1 + rv2 + sa2 + rv3 + sa3) / 3
    return venc_a, venc_b

def gerar_pdf_documentos(nome, checklist):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Documentos em falta – {nome}", ln=True, align="L")
    pdf.ln(5)
    for doc in checklist:
        if doc["Estado"] == "FALTA":
            linha = f"{doc['Documento']}: FALTA – {doc['Observacoes']}"
            pdf.set_text_color(255, 0, 0)
            pdf.cell(200, 10, linha, ln=True, align="L")
    file_path = f"/mnt/data/documentos_faltam_{nome.replace(' ', '_')}.pdf"
    pdf.output(file_path)
    return file_path

def proposta_avalista():
    st.title("📄 1º Avalista – Dados")

    df_clientes = carregar_clientes()
    lista_nomes = df_clientes["Nome"].tolist()

    modo = st.radio("Modo", ["Criar novo titular", "Editar titular existente"])

    if modo == "Editar titular existente":
        nome_escolhido = st.selectbox("Selecionar cliente", lista_nomes)
        dados = df_clientes[df_clientes["Nome"] == nome_escolhido].iloc[0]
        nif = dados["NIF"]
        nome = dados["Nome"]
        data_nasc = datetime.strptime(dados["Data_Nascimento"], "%Y-%m-%d").date()
    else:
        nome_escolhido = ""
        nif = ""
        nome = ""
        data_nasc = date.today()

    with st.form("form_avalista"):

        st.subheader("🪪 Documento de Identificação")
        col1, col2, col3 = st.columns(3)
        with col1:
            input_nif = st.text_input("NIF", value=nif)
        with col2:
            tipo_doc = st.selectbox("Tipo de Identificação", [
                "Autorização residência", "Título residência", "Cartão Cidadão", "Cartão Cidadão Porto Seguro"
            ])
        with col3:
            num_ident = st.text_input("Nº Identificação", max_chars=13)

        col4, col5, col6 = st.columns(3)
        with col4:
            validade = st.date_input("Data de Validade", min_value=date(2022,1,1), max_value=date(2050,12,31))
        with col5:
            entidade = st.text_input("Entidade Emitente")
        with col6:
            pais_emissao = st.text_input("País de Emissão")

        input_niss = st.text_input("Nº Segurança Social", max_chars=11)

        st.subheader("👤 Dados Pessoais")
        input_nome = st.text_input("Nome Completo", value=nome)
        col7, col8, col9 = st.columns(3)
        with col7:
            genero = st.selectbox("Género", ["Masculino", "Feminino"])
        with col8:
            nascimento = st.date_input("Data de Nascimento", value=data_nasc, min_value=date(1940, 1, 1), max_value=date.today())
        with col9:
            nacionalidade = st.text_input("Nacionalidade")

        col10, col11, col12 = st.columns(3)
        with col10:
            outras_nac = st.selectbox("Outras Nacionalidades", ["Não", "Sim"])
        with col11:
            naturalidade = st.text_input("Naturalidade")
        with col12:
            estado_civil = st.selectbox("Estado Civil", ["Casado", "Divorciado", "Separado", "Solteiro", "Viúvo"])

        col13, col14 = st.columns(2)
        with col13:
            dependentes = st.number_input("Número de Dependentes", min_value=0, step=1)
        with col14:
            habilitacoes = st.selectbox("Habilitações", ["Primária", "Secundária", "Universitária"])

        st.subheader("📞 Contactos")
        col15, col16, col17 = st.columns(3)
        with col15:
            cp = st.text_input("Código Postal", placeholder="0000-000")
        with col16:
            morada = st.text_input("Morada")
        with col17:
            porta = st.text_input("Porta")

        col18, col19, col20 = st.columns(3)
        with col18:
            andar = st.text_input("Andar")
        with col19:
            localidade = st.text_input("Localidade")
        with col20:
            morada_igual = st.selectbox("Morada igual à fiscal?", ["Sim", "Não"])

        col21, col22, col23 = st.columns(3)
        with col21:
            tipo_hab = st.selectbox("Tipo Habitação", [
                "Arrendada", "Profissional", "Familiares",
                "Própria com hipoteca", "Própria sem hipoteca", "Sem domicilio"
            ])
        with col22:
            telefone_fixo = st.text_input("Telefone Fixo", max_chars=9)
        with col23:
            telemovel = st.text_input("Telemóvel", max_chars=9)

        email = st.text_input("E-Mail")

        if input_nif and input_nome:
            identificador = gerar_identificador(input_nif, input_nome)
            st.text_input("Identificador da Proposta", value=identificador, disabled=True)

        st.subheader("💼 Dados Profissionais")
        col1, col2 = st.columns(2)
        with col1:
            profissao = st.text_input("Profissão")
        with col2:
            antiguidade = st.date_input("Antiguidade", min_value=date(1940,1,1), max_value=date.today())

        col3, col4 = st.columns(2)
        with col3:
            contrato = st.selectbox("Contrato de Trabalho", [
                "A prazo (Função pública)", "Contrato a prazo", "Contrato efetivo", "Trabalho temporário", "ENI"
            ])
        with col4:
            nipc = st.text_input("NIPC", max_chars=9)

        col5, col6 = st.columns(2)
        with col5:
            empresa = st.text_input("Nome da Empresa")
        with col6:
            telefone_emp = st.text_input("Telefone da Empresa", max_chars=9)

        col7, col8 = st.columns(2)
        with col7:
            cae = st.text_input("CAE do Empregador", max_chars=5)
        with col8:
            atividade = st.text_input("Atividade do Empregador")

        st.subheader("💶 Rendimentos")
        duodecimos = st.selectbox("Duodécimos", ["Sim", "Não"])
        colr1, colr2, colr3 = st.columns(3)
        with colr1:
            rv1 = st.number_input("Recibo mês -1", step=1.0)
            sa1 = st.number_input("Subsídio mês -1", step=1.0)
        with colr2:
            rv2 = st.number_input("Recibo mês -2", step=1.0)
            sa2 = st.number_input("Subsídio mês -2", step=1.0)
        with colr3:
            rv3 = st.number_input("Recibo mês -3", step=1.0)
            sa3 = st.number_input("Subsídio mês -3", step=1.0)

        venc_a, venc_b = calcular_vencimentos(duodecimos, rv1, rv2, rv3, sa1, sa2, sa3)
        col_va, col_vb = st.columns(2)
        with col_va:
            st.metric("Vencimento Líquido A (€)", f"{venc_a:.2f}")
        with col_vb:
            st.metric("Vencimento Líquido B (€)", f"{venc_b:.2f}")

        st.subheader("📋 Checklist de Documentos")
        documentos = [
            "Identificação", "3 recibos vencimento", "Comprovativo IBAN", "Comprovativo de Morada",
            "3 extratos bancários", "Contrato trabalho", "Declaração Início Atividade",
            "Passaporte", "Mod. 3 IRS"
        ]
        checklist = []
        for doc in documentos:
            col1, col2 = st.columns([1, 2])
            with col1:
                estado = st.selectbox(f"{doc}", ["OK", "FALTA"], key='av_'+doc)
            with col2:
                obs = st.text_input(f"Observações {doc}", key='av_'+doc + "_obs")
            checklist.append({"Documento": doc, "Estado": estado, "Observacoes": obs})

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            gravar = st.form_submit_button("💾 Gravar / Atualizar")
        with col_btn2:
            gerar_pdf = st.form_submit_button("🧾 Gerar PDF Documentos em Falta")

        if gerar_pdf and input_nome:
            caminho_pdf = gerar_pdf_documentos(input_nome, checklist)
            st.success(f"PDF gerado com sucesso.")
            st.markdown(f"[📄 Abrir PDF]({caminho_pdf})")
