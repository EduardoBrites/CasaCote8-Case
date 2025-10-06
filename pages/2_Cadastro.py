import streamlit as st
import requests
import datetime
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

st.title("Cadastro de informações")
st.divider()

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
        nome_proj = st.text_input("Nome do projeto")
        prazo_proj_date = st.date_input("Prazo de entrega")
        prazo_proj = prazo_proj_date.isoformat()
        try:
            response = requests.get(api_url+"clientes/")
            clientes = response.json() if response.status_code == 200 else []
        except Exception as e:
            st.error(f"Erro ao buscar clientes: {e}")
            clientes = []
        
        if clientes:
            options = [(c["id_cli"], f"{c['nome_cli']} ({c['email_cli']})") for c in clientes]
            selected = st.selectbox("Cliente", options, format_func=lambda x: x[1])
            cliente_id_cli = selected[0]
        else:
            st.warning("Sem clientes cadastrados!")
            
        if st.button(label = "Cadastrar projeto", type="primary"):
            projeto_data = {
                "nome_proj": nome_proj,
                "cliente_id_cli": cliente_id_cli,
                "prazo_proj": prazo_proj
            }
            try:
                response = requests.post(api_url+"projetos/", json=projeto_data)
                if response.status_code == 200:
                    st.success("Projeto cadastrado com sucesso!")
                else:
                    st.error(f"Erro ao cadastrar: {response.text}")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")
    
    with col3:
        try:
            response = requests.get(api_url+"projetos/")
            projetos = response.json() if response.status_code == 200 else []
        except Exception as e:
            st.error(f"Erro ao buscar projetos: {e}")
            projetos = []
        
        if projetos:
            options = [(p["id_proj"], f"{p['nome_proj']}") for p in projetos]
            selected = st.selectbox("Projeto", options, format_func=lambda x: x[1])
            projeto_id_proj = selected[0]
        else:
            st.warning("Sem projetos cadastrados!")
        
        try:
            response = requests.get(api_url+"fornecedores/")
            fornecedores = response.json() if response.status_code == 200 else []
        except Exception as e:
            st.error(f"Erro ao buscar fornecedores: {e}")
            fornecedores = []
        
        if fornecedores:
            options = [(f["id_fornec"], f"{f['nome_fornec']} ({f['email_fornec']})") for f in fornecedores]
            selected = st.selectbox("Fornecedor", options, format_func=lambda x: x[1])
            produto_fornecedor_id_fornec = selected[0]
        else:
            st.warning("Sem fornecedores cadastrados!")
            
        try:
            response = requests.get(api_url+"produtos/")
            produtos = response.json() if response.status_code == 200 else []
        except Exception as e:
            st.error(f"Erro ao buscar produtos: {e}")
            produtos = []
        
        if produtos:
            options = [(p["fornecedor_id_fornec"], p["id_prod"], p["colecao_prod"], p["cor_prod"], f"{p['nome_prod']}") for p in produtos if p["fornecedor_id_fornec"] == produto_fornecedor_id_fornec]
            selected = st.selectbox("Produto", options, format_func=lambda x: f"{x[4]} ({x[3]})")
            produto_id_prod = selected[0]
        else:
            st.warning("Sem produtos cadastrados!")
        
        quantidade_prod = st.number_input(label="Quantidade", format="%0i")
        if st.button(label = "Adicionar"):
            projetoproduto_data = {
            "projeto_id_proj": projeto_id_proj,
            "produto_id_prod": produto_id_prod,
            "produto_fornecedor_id_fornec": produto_fornecedor_id_fornec,
            "quantidade_prod": quantidade_prod
            }
            try:
                response = requests.post(api_url+"projetosprodutos/", json=projetoproduto_data)
                if response.status_code == 200:
                    st.success("Produto cadastrado no projeto com sucesso!")
                else:
                    st.error(f"Erro ao cadastrar: {response.text}")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")

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
        
        if fornecedores:
            options = [(f["id_fornec"], f"{f['nome_fornec']} ({f['email_fornec']})") for f in fornecedores]
            selected = st.selectbox("Fornecedor", options, format_func=lambda x: x[1])
            fornecedor_id_fornec = selected[0]
        else:
            st.warning("Sem fornecedores cadastrados!")
            
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