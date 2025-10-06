import streamlit as st
import requests
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="CasaCote8 - Financeiro", 
    layout="wide")

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #ff000050;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("./assets/img/CasaCote8Logo.png", use_container_width=True)

api_url = "http://127.0.0.1:8000"

def listar_projetos():
    try:
        r = requests.get(f"{api_url}/projetos/")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Erro ao buscar projetos: {e}")
        return []

def obter_lucro(projeto_id: int):
    try:
        r = requests.get(f"{api_url}/lucro/{projeto_id}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Erro ao calcular lucro: {e}")
        return None


projetos = listar_projetos()
if not projetos:
    st.warning("Nenhum projeto encontrado. Verifique se o backend está rodando e o endpoint /projetos/ existe.")
else:
    options = {p.get("id_proj", p.get("id", None)): p.get("nome_proj", p.get("nome", "Projeto sem nome")) for p in projetos}
    projeto_id = st.selectbox("Selecione o projeto", options=list(options.keys()), format_func=lambda x: options.get(x, str(x)))

    if st.button("Calcular Lucro"):
        resultado = obter_lucro(projeto_id)
        if resultado:
            detalhes = resultado.get("detalhes", [])
            total = resultado.get("total_lucro", 0.0)

            if len(detalhes)==0:
                st.info("Nenhum produto cadastrado para este projeto.")
            else:
                df = pd.DataFrame(detalhes)
                st.subheader("Detalhes por produto")
                st.dataframe(df[["produto_nome","quantidade","preco_unitario","lucro_item"]].rename(columns={
                    "produto_nome":"Produto",
                    "quantidade":"Quantidade",
                    "preco_unitario":"Preço Unitário",
                    "lucro_item":"Lucro"
                }))

                
                st.metric("Lucro Total", f"R$ {total:,.2f}")

                fig = px.bar(df, x="produto_nome", y="lucro_item", labels={"produto_nome":"Produto","lucro_item":"Lucro"}, title="Lucro por produto")
                st.plotly_chart(fig, use_container_width=True)


st.subheader("Lucro Total por Mês")

if st.button("Visualizar Lucro Mensal"):
    try:
        r = requests.get(f"{api_url}/lucro_mensal/")
        r.raise_for_status()
        dados = r.json()

        if not dados:
            st.info("Nenhum dado de lucro mensal encontrado.")
        else:
            df = pd.DataFrame(dados)
            df["mês/ano"] = df["mes"].astype(str) + "/" + df["ano"].astype(str)

            st.dataframe(df[["mês/ano", "lucro_total"]].rename(columns={"mês/ano": "Mês/Ano", "lucro_total": "Lucro Total"}))

            fig = px.bar(df, x="mês/ano", y="lucro_total", title="Lucro Total por Mês", labels={"lucro_total": "Lucro Total", "mês/ano": "Mês/Ano"})
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar lucro mensal: {e}")