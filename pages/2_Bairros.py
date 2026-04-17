import streamlit as st
import plotly.express as px

from services.athena import run_query
from services.queries import get_bairro_query

st.title("Análise por Bairros")
st.caption("Compare bairros por quantidade de imóveis, valor médio estimado e IPTU médio.")

with st.sidebar:
    st.markdown("## Filtros")
    ano = st.selectbox("Ano do exercício", ["2025"], key="ano_bairros")

df = run_query(get_bairro_query(ano))

if df.empty:
    st.warning("Sem dados disponíveis para bairros.")
    st.stop()

bairros_disponiveis = sorted(df["bairro"].dropna().unique().tolist())
bairros_selecionados = st.multiselect("Filtrar bairros", bairros_disponiveis)

if bairros_selecionados:
    df = df[df["bairro"].isin(bairros_selecionados)]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ranking por valor médio do imóvel")
    top_valor = df.sort_values("avg_valor_imovel_estimado", ascending=False).head(10)
    fig_valor = px.bar(
        top_valor,
        x="bairro",
        y="avg_valor_imovel_estimado",
        text_auto=".2s"
    )
    fig_valor.update_layout(
        xaxis_title="Bairro",
        yaxis_title="Valor médio estimado",
        height=450
    )
    st.plotly_chart(fig_valor, use_container_width=True)

with col2:
    st.subheader("Ranking por IPTU médio")
    top_iptu = df.sort_values("avg_valor_iptu", ascending=False).head(10)
    fig_iptu = px.bar(
        top_iptu,
        x="bairro",
        y="avg_valor_iptu",
        text_auto=".2s"
    )
    fig_iptu.update_layout(
        xaxis_title="Bairro",
        yaxis_title="IPTU médio",
        height=450
    )
    st.plotly_chart(fig_iptu, use_container_width=True)

st.subheader("Relação entre valor do imóvel e IPTU")
fig_scatter = px.scatter(
    df,
    x="avg_valor_imovel_estimado",
    y="avg_valor_iptu",
    size="qtd_imoveis",
    hover_name="bairro"
)
fig_scatter.update_layout(
    xaxis_title="Valor médio estimado",
    yaxis_title="IPTU médio",
    height=500
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Detalhamento por bairro")
st.dataframe(df, use_container_width=True)