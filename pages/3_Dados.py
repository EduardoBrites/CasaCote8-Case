import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="CasaCote8 - Procurar", 
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
        background-color: #A1B4B5 !important;
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

st.markdown("""
    <h1>Dados</h1>
""", unsafe_allow_html=True)

st.divider()

#API
api_url = "http://127.0.0.1:8000/"

try:
    response = requests.get(api_url + "fornecedores/")
    fornecedores = response.json() if response.status_code == 200 else []
    df_fornecedores = pd.DataFrame(fornecedores)
except Exception as e:
    st.error(f"Erro ao buscar fornecedores: {e}")
    df_fornecedores = pd.DataFrame()
try:
    response = requests.get(api_url + "clientes/")
    clientes = response.json() if response.status_code == 200 else []
    df_clientes = pd.DataFrame(clientes)
except Exception as e:
    st.error(f"Erro ao buscar clientes: {e}")
    df_clientes = pd.DataFrame()
try:
    response = requests.get(api_url + "produtos/")
    produtos = response.json() if response.status_code == 200 else []
    df_produtos = pd.DataFrame(produtos)
except Exception as e:
    st.error(f"Erro ao buscar produtos: {e}")
    df_produtos = pd.DataFrame()
    
try:
    response = requests.get(api_url + "projetos/")
    projetos = response.json() if response.status_code == 200 else []
    df_projetos = pd.DataFrame(projetos)
except Exception as e:
    st.error(f"Erro ao buscar projetos: {e}")
    df_projetos = pd.DataFrame()

try:
    response = requests.get(api_url + "projetosprodutos/")
    projetosprodutos = response.json() if response.status_code == 200 else []
    df_projetosprodutos = pd.DataFrame(projetosprodutos)
except Exception as e:
    st.error(f"Erro ao buscar os produtos de cada projeto: {e}")
    df_projetosprodutos = pd.DataFrame()

with st.sidebar:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("./assets/img/CasaCote8Logo.png", use_container_width=True)

endpoint_map = {
    "Clientes": "clientes/",
    "Fornecedores": "fornecedores/",
    "Produtos": "produtos/",
    "Projetos": "projetos/",
    "ProjetoProduto": "projetosprodutos/"
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

def select_colunas(colunas):
    colunas_selecionadas = select(ordem(colunas))
    
    if not colunas_selecionadas:
        st.warning("Selecione as colunas para mostrar")
    else:
        st.dataframe(df[colunas_selecionadas], use_container_width=True, column_order=ordem(colunas), height=250)

def mostrar_tabela(df, opcao, df_fornecedores, df_clientes, df_produtos, df_projetos, df_projetosprodutos):
    
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
            
            select_colunas(colunas)
            
        case "Fornecedores":
            colunas = {
                "id_fornec": "Id",
                "nome_fornec": "Nome",
                "tel_fornec": "Telefone",
                "cpfcnpj_fornec": "CPF / CNPJ",
                "email_fornec": "Email"
            }
            df.rename(columns = colunas, inplace = True)
            
            select_colunas(colunas)
            
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
                
            if not df_fornecedores.empty:
                df_fornecedores = df_fornecedores.rename(columns={"id_fornec": "Fornecedor", "nome_fornec": "Nome Fornecedor"})
                df = df.merge(df_fornecedores[["Fornecedor", "Nome Fornecedor"]], on="Fornecedor", how="left")
                df.drop(columns=["Fornecedor"], inplace=True)
                df.rename(columns={"Nome Fornecedor": "Fornecedor"}, inplace=True)
            
            select_colunas(colunas)
            
        case "Projetos":
            colunas = {
                "id_proj": "Id",
                "nome_proj": "Nome",
                "cliente_id_cli": "Cliente",
                "prazo_proj": "Prazo"
            }
            df.rename(columns = colunas, inplace = True)
                
            if not df_clientes.empty:
                df_clientes = df_clientes.rename(columns={"id_cli": "Cliente", "nome_cli": "Nome Cliente"})
                df = df.merge(df_clientes[["Cliente", "Nome Cliente"]], on="Cliente", how="left")
                df.drop(columns=["Cliente"], inplace=True)
                df.rename(columns={"Nome Cliente": "Cliente"}, inplace=True)
            
            select_colunas(colunas)

            # Itens dentro dos projetos
            
            if not df_projetosprodutos.empty:
                colunas_rel = {
                    "projeto_id_proj": "Projeto",
                    "produto_id_prod": "Produto",
                    "produto_fornecedor_id_fornec": "Fornecedor",
                    "quantidade_prod": "Quantidade"
                }
                df_projetosprodutos.rename(columns=colunas_rel, inplace=True)
                
                st.subheader("Itens no projeto")
                
                if projetos:
                    options = [(p["id_proj"], f"{p['nome_proj']}") for p in projetos]
                    selected = st.selectbox("Projeto", options, format_func=lambda x: x[1])
                    projeto_id_proj = selected[0]
                else:
                    st.warning("Sem projetos cadastrados!")

                df_projetosprodutos = df_projetosprodutos[df_projetosprodutos["Projeto"] == projeto_id_proj]

                if not df_projetos.empty:
                    df_projetos_aux = df_projetos.rename(columns={"id_proj": "Projeto", "nome_proj": "Nome Projeto"})
                    df_projetosprodutos = df_projetosprodutos.merge(
                        df_projetos_aux[["Projeto", "Nome Projeto"]],
                        on="Projeto", how="left"
                    )
                if not df_produtos.empty:
                    df_produtos_aux = df_produtos.rename(columns={"id_prod": "Produto", "nome_prod": "Nome Produto"})
                    df_projetosprodutos = df_projetosprodutos.merge(
                        df_produtos_aux[["Produto", "Nome Produto"]],
                        on="Produto", how="left"
                    )
                if not df_fornecedores.empty:
                    df_fornecedores_aux = df_fornecedores.rename(columns={"id_fornec": "Fornecedor", "nome_fornec": "Nome Fornecedor"})
                    df_projetosprodutos = df_projetosprodutos.merge(
                        df_fornecedores_aux[["Fornecedor", "Nome Fornecedor"]],
                        on="Fornecedor", how="left"
                    )

                ordem = ["Nome Projeto", "Nome Fornecedor", "Nome Produto", "Quantidade"]
                
                df_projetosprodutos = df_projetosprodutos[ordem]

                if df_projetosprodutos.empty:
                    st.info("Nenhum item cadastrado neste projeto.")
                else:
                    colunas_selecionadas = select(ordem)
                    if not colunas_selecionadas:
                        st.warning("Selecione as colunas para mostrar")
                    else:
                        st.dataframe(
                            df_projetosprodutos[colunas_selecionadas],
                            use_container_width=True,
                            column_order=ordem
                        )

def listar_dados(ids, nome, msg, dataframe):
    options = [(p[ids], p[nome]) for p in dataframe]
    selected_row = st.selectbox(f"{msg} a excluir", options, format_func=lambda x: f"{x[1]} ({x[0]})")
    
    return selected_row[0]

def remocao_dados(opcao):
    match opcao:
        case "Clientes":
            selected_id_cli = listar_dados("id_cli", "nome_cli", "Cliente", clientes)
            
            if st.button("Deletar"):
                try:
                    response = requests.delete(f"{api_url}clientes/{int(selected_id_cli)}")
                    if response.status_code == 200:
                        st.success("Cliente deletado!")
                        st.rerun()
                    else:
                        st.error("Erro ao deletar cliente")
                except Exception as e:
                    st.error(f"Erro ao conectar com a API: {e}")
                    
        case "Fornecedores":
            selected_id_fornec = listar_dados("id_fornec", "nome_fornec", "Fornecedor", fornecedores)
            
            if st.button("Deletar"):
                try:
                    response = requests.delete(f"{api_url}fornecedores/{int(selected_id_fornec)}")
                    if response.status_code == 200:
                        st.success("Fornecedor deletado!")
                        st.rerun()
                    else:
                        st.error("Erro ao deletar fornecedor")
                except Exception as e:
                    st.error(f"Erro ao conectar com a API: {e}")
                    
        case "Produtos":
            selected_id_proj = listar_dados("id_prod", "nome_prod", "Produto", produtos)
            
            if st.button("Deletar"):
                try:
                    response = requests.delete(f"{api_url}produtos/{int(selected_id_proj)}")
                    if response.status_code == 200:
                        st.success("Produto deletado!")
                        st.rerun()
                    else:
                        st.error("Erro ao deletar produto")
                except Exception as e:
                    st.error(f"Erro ao conectar com a API: {e}")
                    
        case "Projetos":
            selected_id_proj = listar_dados("id_proj", "nome_proj", "Projeto", projetos)
            
            if st.button("Deletar"):
                try:
                    response = requests.delete(f"{api_url}projetos/{int(selected_id_proj)}")
                    if response.status_code == 200:
                        st.success("Projeto deletado!")
                        st.rerun()
                    else:
                        st.error("Erro ao deletar projeto")
                except Exception as e:
                    st.error(f"Erro ao conectar com a API: {e}")
            
            remocao_dados(opcao = "ProjetosProdutos")
        
        case "ProjetosProdutos":
            
            try:
                response = requests.get(api_url+"projetosprodutos/")
                projetosprodutos = response.json() if response.status_code == 200 else []
            except Exception as e:
                st.error(f"Erro ao buscar projetos: {e}")
            
            if projetosprodutos:
                selected_id_proj = st.selectbox("Projeto", [p["id_proj"] for p in projetos])
                selected_id_prod = st.selectbox("Produto", [p["id_prod"] for p in produtos])
                selected_id_fornec = st.selectbox("Fornecedor", [p["id_fornec"] for p in fornecedores])

                if st.button("Deletar Produto", key="delete_prodproj"):
                    try:
                        response = requests.delete(
                            f"{api_url}projetosprodutos/{selected_id_proj}/{selected_id_prod}/{selected_id_fornec}"
                        )
                        if response.status_code == 200:
                            st.success("Item do projeto deletado!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao deletar: {response.text}")
                    except Exception as e:
                        st.error(f"Erro ao conectar com a API: {e}")

if opcao:
    endpoint = endpoint_map[opcao]
    try:
        response = requests.get(api_url + endpoint)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                col1, col2 = st.columns([8, 3]) 
                with col1:
                    mostrar_tabela(df, opcao, df_fornecedores, df_clientes, df_produtos, df_projetos, df_projetosprodutos)
                with col2:
                    remocao_dados(opcao)
                        
            else:
                st.info(f"Nenhum registro encontrado na tabela **{opcao}**.")
        else:
            st.error(f"Erro ao buscar dados ({response.status_code}): {response.text}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
