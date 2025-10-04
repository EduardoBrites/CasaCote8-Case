import streamlit as st
import requests
from fastapi import FastAPI, HTTPException
from sqlmodel import Session
from database.model import Cliente, Fornecedor, Produto, Projeto, ProjetoProduto
from database.banco import engine

st.set_page_config(
    page_title="CasaCote8 - Cadastro", 
    layout="wide")

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #ff000050;
    }
</style>
""", unsafe_allow_html=True)

##API
api_url = "http://127.0.0.1:8000/"

with st.sidebar:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("./assets/img/CasaCote8Logo.png", use_container_width=True)

st.title("Cadastro de infromações")
st.divider()

#col1, col2, col3, col4 = st.columns([1, 3, 6, 1])
#
#with col2:
#    st.selectbox("Clientes", ["André", "Eduardo"])
#    st.button(label = "Cadastrar novo cliente")
#    
#    st.selectbox("Ambiente", ["Lençol", "Capa p/ edredom"])
#    st.button(label = "Cadastrar novo ambiente")
#
#with col3:
#    st.text_area(label = "Descrição do pedido", placeholder = "Escreva aqui as informações adicionais do pedido")
#    st.selectbox("Fornecedores", ["Fornecedor1", "Fornecedor2"])
#    st.multiselect("Cor", ["Azul", "Preto", "Vermelho"])
#    st.number_input(label = "Quantidade", format="%0i")
#    st.number_input(label = "Preço")
#    
#    subcol1, subcol2 = st.columns(2)
#
#    with subcol1:
#        st.number_input(label = "Largura (cm)", format="%0i")
#        
#    with subcol2:
#        st.number_input(label = "Comprimento (cm)", format="%0i")
#    
#    subcol1, subcol2 = st.columns([5, 2])
#    
#    with subcol2:
#        st.write("")
#        st.button(label = "Cadastrar Pedido", type="primary")



col1, col2, col3 = st.columns([1, 5, 1])

with col2:
    tipoCadastro = st.selectbox("Tipo de Cadastro", ["Projetos", "Produtos", "Clientes", "Fornecedores"])
    
col1, col2, col3 = st.columns([5, 1, 7])

if tipoCadastro == "Clientes":
    with col1:
        nome_cli = st.text_input(label="Nome do cliente:")
        tel_cli = st.number_input(label="Telefone", format="%0i", value=None)
        cpfcnpj_cli = st.number_input(label="CPF / CNPJ", format="%0i", value=None)
        email_cli = st.text_input(label="Email")
        if st.button(label = "Cadastrar", type = "primary"):
            cliente_data = {
                "nome_cli": nome_cli,
                "tel_cli": int(tel_cli) if tel_cli else None,
                "cpfcnpj_cli": int(cpfcnpj_cli) if cpfcnpj_cli else 0,
                "email_cli": email_cli 
            }
            try:
                response = requests.post(api_url+"clientes/", json=cliente_data)
                if response.status_code == 200:
                    st.success("Cliente cadastrado com sucesso!")
                else:
                    st.error(f"Erro ao cadastrar: {response.text}")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")

if tipoCadastro == "Projetos":
    with col1:
        prazo_proj = st.date_input(label = "Prazo de entrega")
        try:
            response = requests.get(api_url+"clientes/")
            clientes = response.json() if response.status_code == 200 else []
        except Exception as e:
            st.error(f"Erro ao buscar fornecedores: {e}")
            clientes = []
        options = [(c["id_cli"], f"{c['nome_cli']} ({c['email_cli']})") for c in clientes]
        selected = st.selectbox("Cliente", options, format_func=lambda x: x[1])
        
        cliente_id_cli = selected[0]
        if st.button(label = "Cadastrar projeto", type="primary"):
            projeto_data = {
                "cliente_id_cli": cliente_id_cli,
                "prazo_proj": prazo_proj
            }
            try:
                response = requests.post(api_url+"projeto/", json=projeto_data)
                if response.status_code == 200:
                    st.success("Projeto cadastrado com sucesso!")
                else:
                    st.error(f"Erro ao cadastrar: {response.text}")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")
    
    with col3:
        projeto = st.selectbox("Projetos", ["Projeto", "Projeto1"])
        if projeto != "Projeto":
            st.selectbox("Adicionar produto ao projeto", ["Produto"])
            st.button(label = "Adicionar")

if tipoCadastro == "Produtos":
    with col1:
        nome_prod = st.text_input(label = "Nome do produto")
        cor_prod = st.text_input(label = "Cor")
        colecao_prod = st.text_input(label = "Coleção")
        try:
            response = requests.get(api_url+"fornecedores/")
            fornecedores = response.json() if response.status_code == 200 else []
        except Exception as e:
            st.error(f"Erro ao buscar fornecedores: {e}")
            fornecedores = []
        options = [(f["id_fornec"], f"{f['nome_fornec']} ({f['email_fornec']})") for f in fornecedores]
        selected = st.selectbox("Fornecedor", options, format_func=lambda x: x[1])
        
        fornecedor_id_fornec = selected[0]
        if st.checkbox(label = "Bordado?"):
            bordado_prod = 1
            corlinha_prod = st.text_input(label = "Cor da linha")
        else:
            bordado_prod = 0
            corlinha_prod = None
        precouni_prod = st.number_input(label = "Preço", format="%0.2f")
        
    with col3:
        observacao_prod = st.text_area(label = "Observação", placeholder = "Insira aqui informações edicionais sobre o produto")
        if st.button(label = "Cadastrar produto", type = "primary"):
            produto_data = {
                "fornecedor_id_fornec": fornecedor_id_fornec,
                "nome_prod": nome_prod,
                "cor_prod": cor_prod,
                "colecao_prod": colecao_prod,
                "bordado_prod": bordado_prod,
                "corlinha_prod": corlinha_prod,
                "observacao_prod": observacao_prod,
                "precouni_prod": precouni_prod
            }
            try:
                response = requests.post(api_url+"produtos/", json=produto_data)
                if response.status_code == 200:
                    st.success("Produto cadastrado com sucesso!")
                else:
                    st.error(f"Erro ao cadastrar: {response.text}")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")

if tipoCadastro == "Fornecedores":
    with col1:
        nome_fornec = st.text_input(label = "Nome do fornecedor")
        tel_fornec = st.number_input(label= "Telefone", format="%0i", value=None)
        cpfcnpj_fornec = st.number_input(label= "CPF / CNPJ", format="%0i", value=None)
        email_fornec = st.text_input(label = "Email")
        if st.button(label = "Cadastrar fornecedor", type = "primary"):
            fornecedor_data = {
                "nome_fornec": nome_fornec,
                "tel_fornec": int(tel_fornec) if tel_fornec else None,
                "cpfcnpj_fornec": int(cpfcnpj_fornec) if cpfcnpj_fornec else 0,
                "email_fornec": email_fornec 
            }
            try:
                response = requests.post(api_url+"fornecedores/", json=fornecedor_data)
                if response.status_code == 200:
                    st.success("Fornecedor cadastrado com sucesso!")
                else:
                    st.error(f"Erro ao cadastrar: {response.text}")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")