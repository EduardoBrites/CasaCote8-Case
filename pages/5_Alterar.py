import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="CasaCote8", 
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



def carregar_dados(endpoint):
    try:
        r = requests.get(f"{api_url}/{endpoint}/")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return []


def atualizar_registro(endpoint, id_registro, dados):
    try:
        r = requests.put(f"{api_url}/{endpoint}/{id_registro}", json=dados)
        r.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False


tabela = st.selectbox(
    "Selecione a tabela para alterar dados:",
    ["Cliente", "Fornecedor", "Produto", "Projeto"],
)


# --- Clientes ---
if tabela == "Cliente":
    dados = carregar_dados("clientes")
    if dados:
        df = pd.DataFrame(dados)
        selecionado = st.selectbox("Selecione o cliente:", df["id_cli"].astype(str) + " - " + df["nome_cli"].fillna(""))
        id_cli = int(selecionado.split(" - ")[0])
        cliente = next(c for c in dados if c["id_cli"] == id_cli)

        nome = st.text_input("Nome", cliente.get("nome_cli", ""))
        telefone = st.text_input("Telefone", str(cliente.get("tel_cli") or ""))
        cpfcnpj = st.text_input("CPF/CNPJ", str(cliente.get("cpfcnpj_cli") or ""))
        email = st.text_input("Email", cliente.get("email_cli", ""))

        if st.button("Salvar Alterações"):
            novo = {
                "nome_cli": nome,
                "tel_cli": int(telefone) if telefone else None,
                "cpfcnpj_cli": int(cpfcnpj) if cpfcnpj else None,
                "email_cli": email,
            }
            if atualizar_registro("clientes", id_cli, novo):
                st.success("Cliente atualizado com sucesso!")


# --- Fornecedores ---
elif tabela == "Fornecedor":
    dados = carregar_dados("fornecedores")
    if dados:
        df = pd.DataFrame(dados)
        selecionado = st.selectbox("Selecione o fornecedor:", df["id_fornec"].astype(str) + " - " + df["nome_fornec"].fillna(""))
        id_fornec = int(selecionado.split(" - ")[0])
        fornecedor = next(f for f in dados if f["id_fornec"] == id_fornec)

        nome = st.text_input("Nome", fornecedor.get("nome_fornec", ""))
        telefone = st.text_input("Telefone", str(fornecedor.get("tel_fornec") or ""))
        cpfcnpj = st.text_input("CPF/CNPJ", str(fornecedor.get("cpfcnpj_fornec") or ""))
        email = st.text_input("Email", fornecedor.get("email_fornec", ""))

        if st.button("Salvar Alterações"):
            novo = {
                "nome_fornec": nome,
                "tel_fornec": int(telefone) if telefone else None,
                "cpfcnpj_fornec": int(cpfcnpj) if cpfcnpj else None,
                "email_fornec": email,
            }
            if atualizar_registro("fornecedores", id_fornec, novo):
                st.success("Fornecedor atualizado com sucesso!")


# --- Produtos ---
elif tabela == "Produto":
    dados = carregar_dados("produtos")
    if dados:
        df = pd.DataFrame(dados)
        selecionado = st.selectbox("Selecione o produto:", df["id_prod"].astype(str) + " - " + df["nome_prod"].fillna(""))
        id_prod = int(selecionado.split(" - ")[0])
        produto = next(p for p in dados if p["id_prod"] == id_prod)

        nome = st.text_input("Nome", produto.get("nome_prod", ""))
        cor = st.text_input("Cor", produto.get("cor_prod", ""))
        colecao = st.text_input("Coleção", produto.get("colecao_prod", ""))
        preco = st.number_input("Preço Unitário", value=produto.get("precouni_prod") or 0.0)
        observacao = st.text_area("Observação", produto.get("observacao_prod", ""))

        if st.button("Salvar Alterações"):
            novo = {
                "nome_prod": nome,
                "cor_prod": cor,
                "colecao_prod": colecao,
                "precouni_prod": preco,
                "observacao_prod": observacao,
            }
            if atualizar_registro("produtos", id_prod, novo):
                st.success("Produto atualizado com sucesso!")


# --- Projetos ---
elif tabela == "Projeto":
    dados = carregar_dados("projetos")
    if dados:
        df = pd.DataFrame(dados)
        selecionado = st.selectbox("Selecione o projeto:", df["id_proj"].astype(str) + " - " + df["nome_proj"].fillna(""))
        id_proj = int(selecionado.split(" - ")[0])
        projeto = next(p for p in dados if p["id_proj"] == id_proj)

        nome = st.text_input("Nome", projeto.get("nome_proj", ""))
        prazo = st.date_input("Prazo", pd.to_datetime(projeto.get("prazo_proj")).date() if projeto.get("prazo_proj") else None)

        if st.button("Salvar Alterações"):
            novo = {"nome_proj": nome, "prazo_proj": str(prazo)}
            if atualizar_registro("projetos", id_proj, novo):
                st.success("Projeto atualizado com sucesso!")
