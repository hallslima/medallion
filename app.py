import streamlit as st

st.set_page_config(
    page_title="Dashboard IPTU Recife",
    page_icon="📊",
    layout="wide"
)

st.title("Dashboard IPTU Recife")
st.caption("Análise da camada Gold para indicadores de imóveis, bairros e tipos de uso.")

with st.sidebar:
    st.markdown("## Navegação")
    st.info("Use o menu lateral do Streamlit para acessar as páginas do dashboard.")