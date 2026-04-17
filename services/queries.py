def get_kpis_query(ano: str) -> str:
    return f"""
    SELECT
        COUNT(*) AS qtd_imoveis,
        SUM(valor_imovel_estimado) AS valor_total_imoveis,
        SUM(valor_iptu) AS valor_total_iptu,
        AVG(valor_iptu) AS valor_medio_iptu,
        AVG(valor_imovel_m2_construido) AS valor_medio_m2,
        AVG(area_construida_m2) AS area_media_construida,
        AVG(valor_iptu_sobre_valor_imovel_pct) AS avg_iptu_sobre_valor_pct
    FROM imoveis_analitico
    WHERE ano_exercicio = '"{ano}"'
    """


def get_bairro_query(ano: str) -> str:
    return f"""
    SELECT
        bairro,
        qtd_imoveis,
        avg_area_terreno_m2,
        avg_area_construida_m2,
        sum_valor_imovel_estimado,
        avg_valor_imovel_estimado,
        sum_valor_iptu,
        avg_valor_iptu,
        avg_valor_iptu_m2_construido,
        avg_valor_imovel_m2_construido
    FROM indicadores_bairro
    WHERE ano_exercicio = '"{ano}"'
    ORDER BY avg_valor_iptu DESC
    """


def get_tipo_uso_query(ano: str) -> str:
    return f"""
    SELECT
        tipo_uso_imovel,
        qtd_imoveis,
        avg_area_construida_m2,
        sum_valor_imovel_estimado,
        avg_valor_imovel_estimado,
        sum_valor_iptu,
        avg_valor_iptu,
        avg_valor_iptu_m2_construido
    FROM indicadores_tipo_uso
    WHERE ano_exercicio = '"{ano}"'
    ORDER BY sum_valor_iptu DESC
    """