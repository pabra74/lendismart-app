
import gspread
from google.oauth2.service_account import Credentials

# Autenticação com Google Sheets
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"]
        return gspread.authorize(credentials)

gc = autenticar_gsheets()
sheet = gc.open("LendismartDB")

def gravar_cliente_em_sheet(dados):
    aba = sheet.worksheet("Clientes")
    existentes = aba.col_values(1)  # Coluna 1 = NIF
    if dados["NIF"] in existentes:
        idx = existentes.index(dados["NIF"]) + 1
        aba.update(f"A{idx}:Z{idx}", [list(dados.values())])
    else:
        aba.append_row(list(dados.values()))

def carregar_clientes_de_sheet():
    aba = sheet.worksheet("Clientes")
    registos = aba.get_all_records()
    return registos

import streamlit as st
from gsheets_utils import autenticar_google_sheets, gravar_em_sheet, carregar_todos_de_sheet, obter_colunas
from datetime import date
import re # For input validation
from fpdf import FPDF # For PDF generation

# Configuração da página
st.set_page_config(page_title="Lendismart", layout="wide")

# Estilo do menu lateral
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Menu de navegação
separador = st.sidebar.radio("Navegação", [
    "📄 Proposta", "👥 Clientes", "🏪 Stands", "🚗 Viaturas", "📌 Follow-ups"],
    key="menu_navegacao")

st.sidebar.markdown("---")
sheet = autenticar_google_sheets()

# Cores temáticas por separador
cor_tema = {
    "📄 Proposta": "#e3f2fd",
    "👥 Clientes": "#e8f5e9",
    "🏪 Stands": "#fff3e0",
    "🚗 Viaturas": "#f3e5f5",
    "📌 Follow-ups": "#ede7f6"
}

st.markdown(f"""
    <style>
        .main {{
            background-color: {cor_tema.get(separador)};
        }}
    </style>
""", unsafe_allow_html=True)

# Funções de Validação
def is_valid_nif(nif):
    return re.fullmatch(r"\d{9}", nif) is not None

def is_valid_niss(niss):
    return re.fullmatch(r"\d{11}", niss) is not None

def is_valid_iban(iban):
    return re.fullmatch(r"PT50\d{21}", iban) is not None

def is_valid_contacto(contacto):
    return re.fullmatch(r"\d{9}", contacto) is not None

def is_valid_email(email):
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_codigo_postal(cp):
    return re.fullmatch(r"\d{4}-\d{3}", cp) is not None

def is_valid_nipc(nipc):
    return re.fullmatch(r"\d{9}", nipc) is not None

def is_valid_cae(cae):
    return re.fullmatch(r"\d{5}", cae) is not None

if separador == "📄 Proposta":
    st.header("📄 Proposta")
    col_botoes_1, col_botoes_2, _ = st.columns([1,2,6])
    with col_botoes_1:
        if st.button("Nova Proposta"):
            for key in list(st.session_state.keys()):
                if key.startswith("checklist_") or key.startswith("valor_") or key.startswith("rent_") or key in ["titular1", "titular2", "avalista", "viatura_assoc", "stand_assoc", "estado_proposta"]:
                    del st.session_state[key]
            st.experimental_rerun()
    with col_botoes_2:
        propostas_sheet = carregar_todos_de_sheet(sheet, "Propostas")
    propostas_opcoes = ["Selecionar Proposta Existente"] + [p["id"] for p in propostas_sheet if p.get("id")]
    with col_botoes_2:
        proposta_selecionada = st.selectbox("Carregar Proposta", propostas_opcoes, key="proposta_a_atualizar_select")
        if proposta_selecionada != "Selecionar Proposta Existente":
            proposta = next((p for p in propostas_sheet if p["id"] == proposta_selecionada), None)
            if proposta:
                st.session_state["titular1"] = proposta.get("titular_1", "")
                st.session_state["pvp_proposta"] = float(proposta.get("pvp", 0))
                st.session_state["entrada_proposta"] = float(proposta.get("entrada", 0))
                st.session_state["subvencao_proposta"] = float(proposta.get("subvencao", 0))
                st.session_state["rent_total"] = float(proposta.get("rent_total", 0))
                st.session_state["rent_stand"] = float(proposta.get("rent_stand", 0))
                st.session_state["rent_ic"] = float(proposta.get("ic_pct", 0))
                st.session_state["valor_simulacao"] = float(proposta.get("simulacao", 0))
                st.session_state["seguro"] = proposta.get("seguro", "")
                st.session_state["estado_proposta"] = proposta.get("estado", "")
                st.experimental_rerun()  # Placeholder
        
    
    with st.form("form_proposta"):
        st.subheader("Identificação da Proposta")
        col1, col2 = st.columns(2)
        with col1:
            titular_1 = st.selectbox("Titular 1", ["Selecionar"], key="titular1")
        with col2:
            identificador = f"{titular_1} - ID12345"
            st.text_input("Identificador", value=identificador, disabled=True, key="identificador")

        st.subheader("Associações")
        st.selectbox("Titular 2", ["Selecionar"], key="titular2")
        st.selectbox("Avalista", ["Selecionar"], key="avalista")
        st.selectbox("Viatura Associada", ["Selecionar"], key="viatura_assoc")
        st.selectbox("Stand Associado", ["Selecionar"], key="stand_assoc")

        st.subheader("Valores da Proposta")
        pvp_proposta = st.number_input("PVP (€)", min_value=0.0, format="%.2f", key="pvp_proposta")
        entrada_proposta = st.number_input("Entrada (€)", min_value=0.0, format="%.2f", key="entrada_proposta")
        subvencao_proposta = st.number_input("Subvenção (€)", min_value=0.0, format="%.2f", key="subvencao_proposta")
        valor_a_financiar_calculado = pvp_proposta - entrada_proposta - subvencao_proposta
        st.text_input("Valor a Financiar (€)", value=f"{valor_a_financiar_calculado:.2f}", disabled=True, key="valor_a_financiar_calculado_display")

        st.subheader("📊 Rentabilidade Estimada")
        col3, col4, col5 = st.columns(3)
        with col3:
            total_pct = st.number_input("Rentabilidade Total (%)", 0.0, 100.0, key="rent_total")
        with col4:
            stand_pct = st.number_input("Comissão Stand (%)", 0.0, 100.0, key="rent_stand")
        with col5:
            ic_pct = st.number_input("IC (%)", 0.0, 100.0, key="rent_ic")

        comissao_comercial_pct = 1.5 + max((ic_pct - 3.5) * 0.5, 0)
        comissao_comercial_eur = valor_a_financiar_calculado * comissao_comercial_pct / 100

        col6, col7, col8 = st.columns(3)
        with col6:
            st.text_input("Comissão Comercial (%)", value=f"{comissao_comercial_pct:.2f}", disabled=True, key="comercial_pct")
        with col7:
            st.text_input("Comissão Comercial (€)", value=f"{comissao_comercial_eur:.2f}", disabled=True, key="comercial_eur")
        with col8:
            st.number_input("Valor Simulação (€)", 0.0, 100000.0, key="valor_simulacao")

        st.selectbox("Seguro", ["Sem seguro", "Seguro básico", "Seguro vida mais"], key="seguro")

        st.subheader("Estado da Proposta")
        col_estado1, _ = st.columns(2) # Adjusted as only one field here now
        with col_estado1:
            estado_proposta = st.selectbox("Estado da proposta", ["Enviada BO", "Submetida", "Aguarda docs. adicionais", "Reanálise", "Recusada", "Aprovada", "Financiada"], key="estado_proposta")
        
        st.subheader("Financeiras e Nºs de Proposta")
        financeiras_lista = ["Credibom", "Cetelem", "321 Crédito", "Cofidis", "Banco Primus", "Montepio Crédito", "BBVA", "CA Bank"]
        for fin in financeiras_lista:
            col_fin_1, col_fin_2 = st.columns([2,3])
            with col_fin_1:
                st.text(fin)
            with col_fin_2:
                st.text_input(f"Nº Proposta {fin}", key=f"num_proposta_{fin.lower().replace(' ', '_')}", label_visibility="collapsed")

        st.subheader("Checklist de Documentos Pendentes")
        documentos_pendentes = {
            "Contrato assinado": "contrato_assinado",
            "MUA Venda": "mua_venda",
            "MUA Compra": "mua_compra",
            "DUA/DAV": "dua_dav",
            "Livrança": "livranca",
            "DVI": "dvi"
        }
        for doc_nome, doc_key in documentos_pendentes.items():
            cols_doc_check = st.columns([1, 2, 3])
            with cols_doc_check[0]:
                st.selectbox(" ", ["OK", "Falta"], key=f"checklist_{doc_key}_estado", label_visibility="collapsed")
            with cols_doc_check[1]:
                st.text(doc_nome)
            with cols_doc_check[2]:
                st.text_input("Observações", key=f"checklist_{doc_key}_obs", label_visibility="collapsed")

        st.form_submit_button("Guardar Proposta")

        dados_proposta = {
            "id": identificador,
            "titular_1": titular_1,
            "pvp": pvp_proposta,
            "entrada": entrada_proposta,
            "subvencao": subvencao_proposta,
            "valor_financiar": valor_a_financiar_calculado,
            "rent_total": total_pct,
            "rent_stand": stand_pct,
            "ic_pct": ic_pct,
            "comissao_pct": comissao_comercial_pct,
            "comissao_eur": comissao_comercial_eur,
            "simulacao": st.session_state.get("valor_simulacao", 0),
            "seguro": st.session_state.get("seguro", ""),
            "estado": estado_proposta
        }
        resultado = gravar_em_sheet(sheet, "Propostas", dados_proposta, chave="id")
        st.info(f"Proposta gravada no Google Sheets ({resultado})")


elif separador == "👥 Clientes":
    st.header("👥 Clientes")

    col_botoes_1, col_botoes_2, col_botoes_3, _ = st.columns([1,1,1,4]) 
    with col_botoes_1:
        if st.button("Novo Cliente"):
            for key in list(st.session_state.keys()): # Iterate over a copy of keys
                if key.startswith("cliente_") or key.startswith("prof_") or key.startswith("val_mes") or key.startswith("subs_mes") or key.startswith("doc_") or key.startswith("obs_") or key in ["estado_civil", "tipo_hab", "custo_hab", "num_filhos", "duodecimos", "irs_ano", "valor_ano1", "rend_anu", "checklist_data_cliente"]:
                    del st.session_state[key]
            st.experimental_rerun()
    with col_botoes_2:
        clientes_sheet = carregar_todos_de_sheet(sheet, "Clientes")
    cliente_opcoes = ["Selecionar Cliente Existente"] + [c["id"] + " - " + c["nome"] for c in clientes_sheet if c.get("id")]
    with col_botoes_2:
        cliente_selecionado_atualizar = st.selectbox("Carregar Cliente", cliente_opcoes, key="cliente_a_atualizar_select")
        if cliente_selecionado_atualizar != "Selecionar Cliente Existente":
            cliente_id = cliente_selecionado_atualizar.split(" - ")[0]
            cliente_encontrado = next((c for c in clientes_sheet if c["id"] == cliente_id), None)
            if cliente_encontrado:
                st.session_state["cliente_Nome_Completo"] = cliente_encontrado.get("nome", "")
                st.session_state["cliente_Email"] = cliente_encontrado.get("email", "")
                st.session_state["cliente_Contato"] = cliente_encontrado.get("contacto", "")
                st.session_state["cliente_Tipo_Cliente"] = cliente_encontrado.get("tipo_cliente", "")
                st.session_state["cliente_NISS"] = cliente_encontrado.get("niss", "")
                st.session_state["cliente_IBAN"] = cliente_encontrado.get("iban", "")
                st.session_state["cliente_NIF"] = cliente_encontrado.get("id", "")
                st.session_state["estado_civil"] = cliente_encontrado.get("estado_civil", "")
                st.session_state["tipo_hab"] = cliente_encontrado.get("tipo_hab", "")
                st.session_state["custo_hab"] = float(cliente_encontrado.get("custo_hab", 0))
                st.experimental_rerun() 
        # Placeholder: if 'saved_clients' in st.session_state: clientes_existentes.extend(st.session_state.saved_clients.keys())
        
        # Add logic for actual load button if needed, depends on persistence

    with st.form("form_cliente"):
        st.subheader("Dados Pessoais")
        col_dp1_1, col_dp1_2, col_dp1_3 = st.columns(3)
        with col_dp1_1:
            st.text_input("Nome Completo", key="cliente_Nome_Completo")
        with col_dp1_2:
            st.text_input("Apelido", key="cliente_Apelido")
        with col_dp1_3:
            st.selectbox("Género", ["", "Masculino", "Feminino"], key="cliente_Género")

        col_dp2_1, col_dp2_2, col_dp2_3 = st.columns(3)
        with col_dp2_1:
            st.selectbox("Tipo Cliente", ["", "Particular", "ENI", "Empresa"], key="cliente_Tipo_Cliente")
        with col_dp2_2:
            st.selectbox("Tipo Doc. Identificação", ["", "Cartão Cidadão", "Título de Residência", "CPLP", "Passaporte"], key="cliente_Tipo_Doc_Identificacao")
        with col_dp2_3:
            st.text_input("Nº Identificação", key="cliente_N_Identificacao")

        col_dp3_1, col_dp3_2, col_dp3_3 = st.columns(3)
        with col_dp3_1:
            st.text_input("Entidade Emissora Doc.", key="cliente_Entidade_Emissora_Doc")
        with col_dp3_2:
            st.text_input("País Emissor Doc.", key="cliente_Pais_Emissor_Doc")
        with col_dp3_3:
            st.date_input("Validade Doc.", value=None, key="cliente_Validade_Doc")

        col_dp4_1, col_dp4_2, col_dp4_3 = st.columns(3)
        with col_dp4_1:
            st.date_input("Data Nascimento", value=None, key="cliente_Data_Nascimento")
        with col_dp4_2:
            nif_input = st.text_input("NIF", max_chars=9, key="cliente_NIF")
        with col_dp4_3:
            niss_input = st.text_input("NISS", max_chars=11, key="cliente_NISS")
            
        col_dp5_1, col_dp5_2, col_dp5_3 = st.columns(3)
        with col_dp5_1:
            iban_input = st.text_input("IBAN", placeholder="PT50...", key="cliente_IBAN")
        with col_dp5_2:
            contacto_input = st.text_input("Contato", max_chars=9, key="cliente_Contato")
        with col_dp5_3:
            email_input = st.text_input("Email", key="cliente_Email")

        st.subheader("🏠 Morada e Habitação")
        col_morada_1, col_morada_2, col_morada_3 = st.columns(3)
        with col_morada_1:
            st.text_input("Morada", key="cliente_Morada_Hab")
        with col_morada_2:
            st.text_input("Nº Porta", key="cliente_N_Porta_Hab")
        with col_morada_3:
            st.text_input("Andar", key="cliente_Andar_Hab")
        
        col_morada_4, col_morada_5 = st.columns(2)
        with col_morada_4:
            cp_input = st.text_input("Código Postal", placeholder="XXXX-XXX", key="cliente_Codigo_Postal_Hab")
        with col_morada_5:
            st.text_input("Localidade", key="cliente_Localidade_Hab")
        
        col_hab_1, col_hab_2 = st.columns(2)
        with col_hab_1:
            st.selectbox("Tipo de Habitação", ["", "Arrendada", "Própria com hipoteca", "Própria sem hipoteca", "Profissional", "Casa de Familiares"], key="tipo_hab")
        with col_hab_2:
            st.number_input("Custo mensal da habitação (€)", 0.0, 9999.0, key="custo_hab", format="%.2f")

        st.subheader("👪 Situação Familiar")
        col_fam_1, col_fam_2 = st.columns(2)
        with col_fam_1:
            st.selectbox("Estado civil", ["", "Solteiro", "Casado", "União de facto", "Divorciado", "Viúvo"], key="estado_civil")
        with col_fam_2:
            st.number_input("Nº filhos menores", 0, 20, key="num_filhos", step=1)

        st.subheader("💼 Profissão e Vínculo")
        col_prof1_1, col_prof1_2, col_prof1_3 = st.columns(3)
        with col_prof1_1:
            st.text_input("Tipo contrato de trabalho", key="prof_Tipo_contrato_de_trabalho")
        with col_prof1_2:
            st.date_input("Data início atividade", value=None, key="prof_Data_inicio_atividade")
        with col_prof1_3:
            st.text_input("Antiguidade (anos/meses)", key="prof_Antiguidade")

        col_prof2_1, col_prof2_2, col_prof2_3 = st.columns(3)
        with col_prof2_1:
            st.text_input("Entidade patronal", key="prof_Entidade_patronal")
        with col_prof2_2:
            nipc_input = st.text_input("NIPC (Empresa/ENI)", max_chars=9, key="prof_NIPC")
        with col_prof2_3:
            st.text_input("Telefone entidade", key="prof_Telefone_entidade")
            
        col_prof3_1, col_prof3_2, col_prof3_3 = st.columns(3)
        with col_prof3_1:
            st.text_input("Profissão", key="prof_Profissao")
        with col_prof3_2:
            st.text_input("Atividade", key="prof_Atividade")
        with col_prof3_3:
            cae_input = st.text_input("CAE (Empresa/ENI)", max_chars=5, key="prof_CAE")

        st.subheader("💰 Rendimentos")
        st.radio("Duodécimos", ["Sim", "Não"], key="duodecimos", horizontal=True)
        for mes_idx, mes_label in enumerate(["Mês -1", "Mês -2", "Mês -3"]):
            colr1, colr2 = st.columns(2)
            colr1.number_input(f"Valor recibo {mes_label} (€)", 0.0, key=f"val_mes{mes_idx}", format="%.2f")
            colr2.number_input(f"Subsídio alim. {mes_label} (€)", 0.0, key=f"subs_mes{mes_idx}", format="%.2f")

        st.text_input("Venc. Líquido A (€)", value="0.00", disabled=True, key="vencliq_a")
        st.text_input("Venc. Líquido B (€)", value="0.00", disabled=True, key="vencliq_b")

        st.subheader("📄 IRS e Outros Rendimentos")
        st.radio("Rendimento Anual IRS Ano -1", ["Sim", "Não"], key="irs_ano", horizontal=True)
        st.number_input("Valor Ano -1 (€)", 0.0, key="valor_ano1", format="%.2f")
        for mes_idx, mes_label in enumerate(["Mês -1", "Mês -2", "Mês -3"]):
            st.number_input(f"Valor recibo verde {mes_label} (€)", 0.0, key=f"rec_verde_mes{mes_idx}", format="%.2f")
        st.number_input("Rendimento Anual (€)", 0.0, key="rend_anu", format="%.2f")

        st.subheader("📎 Checklist de Documentos")
        documentos = [
            "Identificação", "3 Recibos Vencimento", "IBAN", "Comprovativo Morada",
            "3 Extratos Bancários", "Contrato Trabalho", "Declaração Início Atividade", "Passaporte", "Mod. 3 IRS"
        ]
        if 'checklist_data_cliente' not in st.session_state:
            st.session_state.checklist_data_cliente = {}

        for doc in documentos:
            colc1, colc2, colc3 = st.columns([1,2,3])
            doc_key_base = f"doc_{doc.lower().replace(' ', '_').replace('.', '')}"
            estado = colc1.selectbox(" ", ["OK", "FALTA"], key=f"{doc_key_base}_estado", label_visibility="collapsed")
            colc2.text(doc)
            obs = colc3.text_input(" ", key=f"{doc_key_base}_obs", label_visibility="collapsed", placeholder="Informações adicionais (ex: Mês de Março)")
            st.session_state.checklist_data_cliente[doc] = {"estado": estado, "obs": obs}

        submitted = st.form_submit_button("Guardar Cliente")
        if submitted:
            valid = True
            if nif_input and not is_valid_nif(nif_input):
                st.error("NIF inválido. Deve conter 9 dígitos.")
                valid = False
            if niss_input and not is_valid_niss(niss_input):
                st.error("NISS inválido. Deve conter 11 dígitos.")
                valid = False
            if iban_input and not is_valid_iban(iban_input):
                st.error("IBAN inválido. Deve estar no formato PT50XXXXXXXXXXXXXXXXXXXXX.")
                valid = False
            if contacto_input and not is_valid_contacto(contacto_input):
                st.error("Contacto telefónico inválido. Deve conter 9 dígitos.")
                valid = False
            if email_input and not is_valid_email(email_input):
                st.error("Formato de E-mail inválido.")
                valid = False
            if cp_input and not is_valid_codigo_postal(cp_input):
                st.error("Código Postal inválido. Deve estar no formato XXXX-XXX.")
                valid = False
            
            tipo_cliente_val = st.session_state.get("cliente_Tipo_Cliente", "")
            if tipo_cliente_val in ["ENI", "Empresa"]:
                if nipc_input and not is_valid_nipc(nipc_input):
                    st.error("NIPC inválido. Deve conter 9 dígitos.")
                    valid = False
                if cae_input and not is_valid_cae(cae_input):
                    st.error("CAE inválido. Deve conter 5 dígitos.")
                    valid = False
            
            if valid:
                gravar_cliente_em_sheet({
                    "NIF": nif_input,
                    "Nome": st.session_state.get("cliente_Nome_Completo", ""),
                    "Apelido": st.session_state.get("cliente_Apelido", ""),
                    "Email": email_input,
                    "Contato": contacto_input,
                    "IBAN": iban_input
                })
                st.success("Cliente guardado com sucesso no Google Sheets!")
    

    
    # Botão PDF reposicionado para o fim do formulário
    if st.button("Gerar PDF Docs. Falta"):
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.set_y(10)
        pdf.set_font_size(8)
        pdf.multi_cell(0, 4, "Lendismart (Logo Placeholder)\nOlá. O meu nome é Paulo Abrantes e sou intermediário de crédito registado no Banco de Portugal.\nTrabalho na empresa Lendismart. N.º registo junto do Banco de Portugal: 0006212.\nA informação relativa ao registo da Lendismart, Unipessoal Lda junto do Banco de Portugal pode ser consultada em: https://www.bportugal.pt/intermediariocreditofar/lendismart-unipessoal-lda")
        pdf.ln(5)

        client_name_pdf = st.session_state.get("cliente_Nome_Completo", "N/A")
        pdf.set_font_size(14)
        pdf.cell(0, 10, f"Cliente: {client_name_pdf}", ln=True, align="C")
        pdf.ln(3)

        pdf.set_font_size(12)
        pdf.cell(0, 8, "Documentos em Falta:", ln=True)
        pdf.set_font_size(10)

        missing_docs_count = 0
        if 'checklist_data_cliente' in st.session_state:
            for doc_name, data in st.session_state.checklist_data_cliente.items():
                if data.get("estado") == "FALTA":
                    missing_docs_count += 1
                    pdf.set_font_size(10)
                    pdf.cell(70, 6, f"{doc_name}", border=1)
                    pdf.cell(30, 6, f"{data['estado']}", border=1)
                    pdf.set_font_size(8)
                    obs_text = data.get('obs', '')
                    pdf.multi_cell(0, 6, f"Info: {obs_text if obs_text else '-'}", border=1, ln=1)
                    pdf.ln(1)

        if missing_docs_count == 0:
            pdf.set_font_size(10)
            pdf.cell(0, 8, "Nenhum documento em falta registado.", ln=True)

        pdf_bytes = pdf.output(dest="S").encode("latin-1")

        st.download_button(
            label="Download PDF Documentos em Falta",
            data=pdf_bytes,
            file_name=f"documentos_faltantes_{client_name_pdf.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
elif separador == "🏪 Stands":
    st.header("🏪 Stands")
    col_botoes_1, col_botoes_2, _ = st.columns([1,2,6])
    with col_botoes_1:
        if st.button("Novo Stand"):
            for key in list(st.session_state.keys()):
                if key.startswith("stand_"):
                    del st.session_state[key]
            st.experimental_rerun()
    with col_botoes_2:
        stands_sheet = carregar_todos_de_sheet(sheet, "Stands")
    stand_opcoes = ["Selecionar Stand Existente"] + [s["id"] + " - " + s["nome_comercial"] for s in stands_sheet if s.get("id")]
    with col_botoes_2:
        stand_selecionado = st.selectbox("Carregar Stand", stand_opcoes, key="stand_a_atualizar_select")
        if stand_selecionado != "Selecionar Stand Existente":
            stand_id = stand_selecionado.split(" - ")[0]
            stand = next((s for s in stands_sheet if s["id"] == stand_id), None)
            if stand:
                st.session_state["stand_nome_com"] = stand.get("nome_comercial", "")
                st.session_state["stand_nome_emp"] = stand.get("empresa", "")
                st.session_state["stand_nif"] = stand.get("id", "")
                st.session_state["stand_resp_nome"] = stand.get("resp_nome", "")
                st.session_state["stand_resp_tlm"] = stand.get("resp_tlm", "")
                st.session_state["stand_resp_email"] = stand.get("resp_email", "")
                st.experimental_rerun()  # Placeholder
        
    
    with st.form("form_stand"):
        col1, col2, col3 = st.columns(3)
        col1.text_input("Nome Comercial", key="stand_nome_com")
        col2.text_input("Nome Empresa", key="stand_nome_emp")
        col3.text_input("NIF", key="stand_nif")

        st.subheader("📞 Principal")
        colp1, colp2, colp3 = st.columns(3)
        colp1.text_input("Nome", key="stand_resp_nome")
        colp2.text_input("Tlm", key="stand_resp_tlm")
        colp3.text_input("E-mail", key="stand_resp_email")

        st.subheader("💼 Vendas")
        colv1, colv2, colv3 = st.columns(3)
        colv1.text_input("Nome", key="stand_vend_nome")
        colv2.text_input("Tlm", key="stand_vend_tlm")
        colv3.text_input("E-mail", key="stand_vend_email")

        st.subheader("💳 Financeiro")
        colf1, colf2, colf3 = st.columns(3)
        colf1.text_input("Nome", key="stand_fin_nome")
        colf2.text_input("Tlm", key="stand_fin_tlm")
        colf3.text_input("E-mail", key="stand_fin_email")

        st.subheader("🌐 Portais e Redes Sociais")
        st.text_input("Site Institucional", key="stand_site")
        st.text_input("Standvirtual", key="stand_sv")
        st.text_input("OLX", key="stand_olx")
        st.text_input("Carmine", key="stand_carmine")
        st.text_input("Facebook", key="stand_fb")
        st.text_input("Instagram", key="stand_ig")
        st.text_input("TikTok", key="stand_tt")
        st.text_input("Outras redes sociais", key="stand_outras")

        st.form_submit_button("Guardar Stand")

        dados_stand = {
            "id": st.session_state.get("stand_nif", ""),
            "nome_comercial": st.session_state.get("stand_nome_com", ""),
            "empresa": st.session_state.get("stand_nome_emp", ""),
            "resp_nome": st.session_state.get("stand_resp_nome", ""),
            "resp_tlm": st.session_state.get("stand_resp_tlm", ""),
            "resp_email": st.session_state.get("stand_resp_email", "")
        }
        resultado = gravar_em_sheet(sheet, "Stands", dados_stand, chave="id")
        st.info(f"Stand gravado no Google Sheets ({resultado})")


elif separador == "🚗 Viaturas":
    st.header("🚗 Viaturas")
    col_botoes_1, col_botoes_2, _ = st.columns([1,2,6])
    with col_botoes_1:
        if st.button("Nova Viatura"):
            for key in list(st.session_state.keys()):
                if key.startswith("via_") or key in ["pvp", "via_stand", "link_anuncio_viatura"]:
                    del st.session_state[key]
            st.experimental_rerun()
    with col_botoes_2:
        viaturas_sheet = carregar_todos_de_sheet(sheet, "Viaturas")
    viatura_opcoes = ["Selecionar Viatura Existente"] + [v["id"] for v in viaturas_sheet if v.get("id")]
    with col_botoes_2:
        viatura_selecionada = st.selectbox("Carregar Viatura", viatura_opcoes, key="viatura_a_atualizar_select")
        if viatura_selecionada != "Selecionar Viatura Existente":
            viatura = next((v for v in viaturas_sheet if v["id"] == viatura_selecionada), None)
            if viatura:
                st.session_state["via_Matrícula"] = viatura.get("id", "")
                st.session_state["via_Marca"] = viatura.get("marca", "")
                st.session_state["via_Modelo"] = viatura.get("modelo", "")
                st.session_state["via_Versão"] = viatura.get("versao", "")
                st.session_state["via_stand"] = viatura.get("stand", "")
                st.session_state["pvp"] = float(viatura.get("pvp", 0))
                st.session_state["link_anuncio_viatura"] = viatura.get("link", "")
                st.experimental_rerun()  # Placeholder
        
    
    with st.form("form_viatura"):
        for linha in [
            ("Marca", "Modelo", "Versão"),
            ("Cilindrada", "KW", "Nº Chassis"),
            ("Matrícula", "Data Matrícula", "Importado?")
        ]:
            cols = st.columns(3)
            for i, campo in enumerate(linha):
                cols[i].text_input(campo, key=f"via_{campo}")

        colv1, colv2 = st.columns(2)
        colv1.number_input("PVP (€)", 0.0, key="pvp", format="%.2f")
        st.selectbox("Stand Associado", ["Selecionar"], key="via_stand")
        st.text_input("Link Anúncio Viatura", key="link_anuncio_viatura")

        st.form_submit_button("Guardar Viatura")

        dados_viatura = {
            "id": st.session_state.get("via_Matrícula", ""),
            "marca": st.session_state.get("via_Marca", ""),
            "modelo": st.session_state.get("via_Modelo", ""),
            "versao": st.session_state.get("via_Versão", ""),
            "stand": st.session_state.get("via_stand", ""),
            "pvp": st.session_state.get("pvp", 0),
            "link": st.session_state.get("link_anuncio_viatura", "")
        }
        resultado = gravar_em_sheet(sheet, "Viaturas", dados_viatura, chave="id")
        st.info(f"Viatura gravada no Google Sheets ({resultado})")


elif separador == "📌 Follow-ups":
    st.header("📌 Follow-ups")
    col_botoes_1, col_botoes_2, _ = st.columns([1,2,6])
    with col_botoes_1:
        if st.button("Novo Follow-up"):
            for key in list(st.session_state.keys()):
                if key.startswith("follow_") or key == "data_followup" or key == "notas_followup":
                    del st.session_state[key]
            st.experimental_rerun()
    with col_botoes_2:
        followups_sheet = carregar_todos_de_sheet(sheet, "FollowUps")
    followup_opcoes = ["Selecionar Follow-up Existente"] + [f["id"] for f in followups_sheet if f.get("id")]
    with col_botoes_2:
        followup_selecionado = st.selectbox("Carregar Follow-up", followup_opcoes, key="followup_a_atualizar_select")
        if followup_selecionado != "Selecionar Follow-up Existente":
            followup = next((f for f in followups_sheet if f["id"] == followup_selecionado), None)
            if followup:
                st.session_state["data_followup"] = followup.get("id", "")
                st.session_state["follow_cliente"] = followup.get("cliente", "")
                st.session_state["follow_stand"] = followup.get("stand", "")
                st.session_state["notas_followup"] = followup.get("notas", "")
                st.experimental_rerun()  # Placeholder
        
    
    with st.form("form_followup"):
        st.date_input("Data do Follow-up", value=None, key="data_followup")
        st.selectbox("Cliente Associado", ["Selecionar"], key="follow_cliente")
        st.selectbox("Stand Associado", ["Selecionar"], key="follow_stand")
        st.text_area("Notas", key="notas_followup")
        st.form_submit_button("Guardar Follow-up")

        dados_followup = {
            "id": st.session_state.get("data_followup", ""),
            "cliente": st.session_state.get("follow_cliente", ""),
            "stand": st.session_state.get("follow_stand", ""),
            "notas": st.session_state.get("notas_followup", "")
        }
        resultado = gravar_em_sheet(sheet, "FollowUps", dados_followup, chave="id")
        st.info(f"Follow-up gravado no Google Sheets ({resultado})")




