import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="CasaCote8 - Procurar", 
    layout="wide")

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #ff000050;
    }
</style>
""", unsafe_allow_html=True)

#API
api_url = "http://127.0.0.1:8000/"

with st.sidebar:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("./assets/img/CasaCote8Logo.png", use_container_width=True)

endpoint_map = {
    "Clientes": "clientes/",
    "Fornecedores": "fornecedores/",
    "Produtos": "produtos/",
    "Projetos": "projetos/",
    "ProjetoProduto": "projetoproduto/"
}


opcao = st.selectbox(
    "Selecione a tabela para visualizar:",
    ["Clientes", "Fornecedores", "Produtos", "Projetos"]
)

def ordem(colunas):
    ordem = list(colunas.values())
    return ordem

def select(opcoes):
    colunas = st.multiselect("Colunas", opcoes, default=opcoes)
    return colunas

def mostrar_tabela(df, opcao):
    match opcao:
        case "Clientes":
            
            colunas = {
                "id_cli": "Id",
                "nome_cli": "Nome",
                "tel_cli": "Telefone",
                "cpfcnpj_cli": "CPF / CNPJ",
                "email_cli": "Email"
            }
            df.rename(columns = colunas, inplace = True)
            
            colunas_selecionadas = select(ordem(colunas))
            st.dataframe(df[colunas_selecionadas], use_container_width=True, column_order=ordem(colunas))
        case "Fornecedores":
            colunas = {
                "id_fornec": "Id",
                "nome_fornec": "Nome",
                "tel_fornec": "Telefone",
                "cpfcnpj_fornec": "CPF / CNPJ",
                "email_fornec": "Email"
            }
            df.rename(columns = colunas, inplace = True)
            
            colunas_selecionadas = select(ordem(colunas))
            
            if not colunas_selecionadas:
                st.warning("Selecione as colunas para mostrar")
            else:
                st.dataframe(df[colunas_selecionadas], use_container_width=True, column_order=ordem(colunas))
        case "Produtos":
            colunas = {
                "id_prod": "Id",
                "fornecedor_id_fornec": "Fornecedor",
                "nome_prod": "Nome",
                "cor_prod": "Cor",
                "colecao_prod": "Coleção",
                "bordado_prod": "É bordado",
                "corlinha_prod": "Cor do bordado",
                "observacao_prod": "Observação",
                "precouni_prod": "Preço unitário"
            }
            df.rename(columns = colunas, inplace = True)
            
            try:
                response = requests.get(api_url + "fornecedores/")
                fornecedores = response.json() if response.status_code == 200 else []
                df_fornecedores = pd.DataFrame(fornecedores)
            except Exception as e:
                st.error(f"Erro ao buscar fornecedores: {e}")
                df_fornecedores = pd.DataFrame()
                
            if not df_fornecedores.empty:
                df_fornecedores = df_fornecedores.rename(columns={"id_fornec": "Fornecedor", "nome_fornec": "Nome Fornecedor"})
                df = df.merge(df_fornecedores[["Fornecedor", "Nome Fornecedor"]], on="Fornecedor", how="left")
                df.drop(columns=["Fornecedor"], inplace=True)
                df.rename(columns={"Nome Fornecedor": "Fornecedor"}, inplace=True)
            
            colunas_selecionadas = select(ordem(colunas))
            st.dataframe(df[colunas_selecionadas], use_container_width=True, column_order=ordem(colunas))
        case "Projetos":
            colunas = {
                "id_proj": "Id",
                "nome_proj": "Nome",
                "cliente_id_cli": "Cliente",
                "prazo_proj": "Prazo"
            }
            df.rename(columns = colunas, inplace = True)
            
            try:
                response = requests.get(api_url + "clientes/")
                clientes = response.json() if response.status_code == 200 else []
                df_clientes = pd.DataFrame(clientes)
            except Exception as e:
                st.error(f"Erro ao buscar clientes: {e}")
                df_clientes = pd.DataFrame()
                
            if not df_clientes.empty:
                df_clientes = df_clientes.rename(columns={"id_cli": "Cliente", "nome_cli": "Nome Cliente"})
                df = df.merge(df_clientes[["Cliente", "Nome Cliente"]], on="Cliente", how="left")
                df.drop(columns=["Cliente"], inplace=True)
                df.rename(columns={"Nome Cliente": "Cliente"}, inplace=True)
            
            colunas_selecionadas = select(ordem(colunas))
            st.dataframe(df[colunas_selecionadas], use_container_width=True, column_order=ordem(colunas))

if opcao:
    endpoint = endpoint_map[opcao]
    try:
        response = requests.get(api_url + endpoint)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                mostrar_tabela(df, opcao)
            else:
                st.info(f"Nenhum registro encontrado na tabela **{opcao}**.")
        else:
            st.error(f"Erro ao buscar dados ({response.status_code}): {response.text}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
