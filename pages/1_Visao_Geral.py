import streamlit as st
import plotly.express as px

from services.athena import run_query
from services.queries import get_kpis_query, get_bairro_query, get_tipo_uso_query
from utils.formatters import format_brl, format_m2, format_int, format_pct, safe_value

st.title("Visão Geral")
st.caption("Resumo executivo dos principais indicadores do IPTU e dos imóveis analisados.")

with st.sidebar:
    st.markdown("## Filtros")
    ano = st.selectbox("Ano do exercício", ["2025"], key="ano_visao_geral")

kpis = run_query(get_kpis_query(ano))
bairro = run_query(get_bairro_query(ano))
tipo = run_query(get_tipo_uso_query(ano))

if kpis.empty:
    st.warning("Nenhum dado encontrado para a visão geral.")
    st.stop()

row = kpis.iloc[0]

qtd_imoveis = safe_value(row.get("qtd_imoveis"), 0)
valor_total_imoveis = safe_value(row.get("valor_total_imoveis"), 0)
valor_total_iptu = safe_value(row.get("valor_total_iptu"), 0)
valor_medio_iptu = safe_value(row.get("valor_medio_iptu"), 0)
valor_medio_m2 = safe_value(row.get("valor_medio_m2"), 0)
area_media_construida = safe_value(row.get("area_media_construida"), 0)
iptu_sobre_valor_pct = safe_value(row.get("avg_iptu_sobre_valor_pct"), 0)

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

c1.metric("Quantidade de imóveis", format_int(qtd_imoveis))
c2.metric("Valor total dos imóveis", format_brl(valor_total_imoveis))
c3.metric("IPTU total", format_brl(valor_total_iptu))
c4.metric("IPTU médio", format_brl(valor_medio_iptu))
c5.metric("Valor médio por m²", format_brl(valor_medio_m2))
c6.metric("Área média construída", format_m2(area_media_construida))

st.info(
    f"Em média, o IPTU representa {format_pct(iptu_sobre_valor_pct)} do valor estimado dos imóveis analisados."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top bairros por IPTU médio")
    if not bairro.empty:
        top_bairro = bairro.sort_values("avg_valor_iptu", ascending=False).head(10)
        fig_bairro = px.bar(
            top_bairro,
            x="bairro",
            y="avg_valor_iptu",
            text_auto=".2s"
        )
        fig_bairro.update_layout(
            xaxis_title="Bairro",
            yaxis_title="IPTU médio",
            height=450
        )
        st.plotly_chart(fig_bairro, use_container_width=True)

with col2:
    st.subheader("Distribuição por tipo de uso")
    if not tipo.empty:
        fig_tipo = px.pie(
            tipo,
            names="tipo_uso_imovel",
            values="qtd_imoveis"
        )
        fig_tipo.update_layout(height=450)
        st.plotly_chart(fig_tipo, use_container_width=True)

st.subheader("Resumo por bairro")
st.caption("Tabela de apoio para conferência e análise detalhada.")
if not bairro.empty:
    st.dataframe(bairro, use_container_width=True)