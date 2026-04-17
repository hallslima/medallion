import streamlit as st
import awswrangler as wr
import boto3
import pandas as pd


def get_aws_config():
    if "aws" not in st.secrets:
        return None
    return st.secrets["aws"]


@st.cache_resource
def get_boto3_session():
    config = get_aws_config()
    if not config:
        return None

    return boto3.Session(
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config["region"],
    )


@st.cache_data(ttl=600)
def run_query(sql: str) -> pd.DataFrame:
    config = get_aws_config()

    if not config:
        return pd.DataFrame()

    if config["aws_access_key_id"] == "teste":
        return pd.DataFrame()

    session = get_boto3_session()

    try:
        df = wr.athena.read_sql_query(
            sql=sql,
            database=config["athena_database"],
            boto3_session=session,
            workgroup=config["athena_workgroup"],
            s3_output=config["s3_output"],
            ctas_approach=False,
        )
        return df
    except Exception as e:
        st.error(f"Erro ao consultar o Athena: {e}")
        return pd.DataFrame()