import streamlit as st
import requests
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="CasaCote8 - Financeiro", 
    layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Nata+Sans:wght@100..900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 100;
        font-size: 15px;
    }
    
    [data-testid="stSidebar"] {
        background-color: #624837;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] a,  
    [data-testid="stSidebar"] div {
        margin-bottom: 7px;
    }
    
    [data-testid="stSidebar"] a {
    }

    [data-testid="stSidebar"] a:hover {
        background-color: rgba(255, 255, 255, 0.15);
    }
    
    .subtext{
        text-align: center;
        border-bottom: 5px solid #365F61;
        font-weight: normal !important;
        font-size: 17px !important;
        letter-spacing: 2px;
        color: ##A18E82 !important;
        padding: 3px 0 3px 0 !important;
        border-radius: 2px;
        text-transform: uppercase;
    }
    
    .text{
        text-align: justify;
    }
    
    h1 {
            text-align: center;
            background-color: #A18E82;
            font-weight: normal !important;
            letter-spacing: 10px;
            color: white !important;
            padding: 10px 0 10px 0 !important;
            width: 100%;    
            border-radius: 2px;
        }
    
    .stButton>button {
        background-color: #365F61 !important;
        color: white !important;
        border-radius: 8px;
        padding: 8px 20px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        background-color: #A1B4B5 !important; /* hover */
    }
    
    .stButton.secondary>button {
        background-color: white !important;
        color: #365F61 !important;
        border: 2px solid #365F61 !important;
    }

    .stButton.secondary>button:hover {
        background-color: #A1B4B5 !important;
        color: white !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #A1B4B5 !important;
        color: white !important;
        border-radius: 6px;
    }
    
    div[data-baseweb="select"] > div:focus-within {
        outline: none !important;
        box-shadow: none !important;
        border: 2px solid transparent !important;
    }

    div[data-baseweb="select"] span {
        color: white !important;
    }
    
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("./assets/img/CasaCote8Logo.png", use_container_width=True)

st.markdown("""
    <h1>Financeiro</h1>
""", unsafe_allow_html=True)

st.divider()

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
    st.warning("Nenhum projeto encontrado.")
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