import streamlit as st
import plotly.express as px

from services.athena import run_query
from services.queries import get_tipo_uso_query

st.title("Análise por Tipo de Uso")
st.caption("Entenda o comportamento dos imóveis por categoria de uso.")

with st.sidebar:
    st.markdown("## Filtros")
    ano = st.selectbox("Ano do exercício", ["2025"], key="ano_tipo")

df = run_query(get_tipo_uso_query(ano))

if df.empty:
    st.warning("Sem dados disponíveis para tipo de uso.")
    st.stop()

tipos_disponiveis = sorted(df["tipo_uso_imovel"].dropna().unique().tolist())
tipos_selecionados = st.multiselect("Filtrar tipo de uso", tipos_disponiveis)

if tipos_selecionados:
    df = df[df["tipo_uso_imovel"].isin(tipos_selecionados)]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Quantidade de imóveis por tipo")
    fig_qtd = px.bar(
        df,
        x="tipo_uso_imovel",
        y="qtd_imoveis",
        text_auto=True
    )
    fig_qtd.update_layout(
        xaxis_title="Tipo de uso",
        yaxis_title="Quantidade de imóveis",
        height=450
    )
    st.plotly_chart(fig_qtd, use_container_width=True)

with col2:
    st.subheader("IPTU total por tipo")
    fig_iptu_total = px.bar(
        df,
        x="tipo_uso_imovel",
        y="sum_valor_iptu",
        text_auto=".2s"
    )
    fig_iptu_total.update_layout(
        xaxis_title="Tipo de uso",
        yaxis_title="IPTU total",
        height=450
    )
    st.plotly_chart(fig_iptu_total, use_container_width=True)

st.subheader("Comparativo de IPTU médio por tipo")
fig_iptu_medio = px.bar(
    df,
    x="tipo_uso_imovel",
    y="avg_valor_iptu",
    text_auto=".2s"
)
fig_iptu_medio.update_layout(
    xaxis_title="Tipo de uso",
    yaxis_title="IPTU médio",
    height=450
)
st.plotly_chart(fig_iptu_medio, use_container_width=True)

st.subheader("Detalhamento por tipo de uso")
st.dataframe(df, use_container_width=True)