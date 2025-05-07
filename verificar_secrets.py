import streamlit as st

st.title("🔐 Teste de Secrets no Streamlit Cloud")

if "gcp_service_account" in st.secrets:
    st.success("✅ A chave 'gcp_service_account' foi carregada com sucesso.")
    st.subheader("🧾 Conteúdo parcial:")
    st.json({k: v for k, v in st.secrets["gcp_service_account"].items() if k != "private_key"})
    
    st.subheader("🔒 Validação da chave privada:")
    pk = st.secrets["gcp_service_account"].get("private_key", "")
    if pk.startswith("-----BEGIN PRIVATE KEY-----") and pk.endswith("-----END PRIVATE KEY-----"):
        st.success("✅ Formato da chave privada parece correto.")
    else:
        st.error("❌ A chave privada NÃO está no formato correto.")
else:
    st.error("❌ 'gcp_service_account' não foi encontrado em st.secrets.")