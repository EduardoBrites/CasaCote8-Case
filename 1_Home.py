import streamlit as st

st.set_page_config(
    page_title="CasaCote8", 
    layout="wide"
)

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
    
    .maintext{
        text-align: center;
        background-color: #365F61;
        font-weight: normal !important;
        font-size: 17px !important;
        letter-spacing: 2px;
        color: white !important;
        padding: 3px 0 3px 0 !important;
        border-radius: 2px;
        text-transform: uppercase;
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
    
    .text2{
        text-align: center;
        color: rgb(240, 240, 240) !important;
        background-color: #A1B4B5;
        border-radius: 2px;
        padding: 3px;
        height: 110px;
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
    
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.image("./assets/img/CasaCote8Logo.png", use_container_width=True)

st.markdown("""
    <h1>Bem Vindo</h1>
""", unsafe_allow_html=True)
    
st.write("")
st.divider()

col1, col2, col3 = st.columns([1, 15, 1])

with col2:
    st.markdown("""
        <p class="maintext">Como navegar</p>

        <p class="text">Esse site tem como objetivo oferecer um sistema organizacional de cadastro, leitura, edição e exclusão de dados, 
            além de contar também com um sistema de análise de dados.</p>
    """, unsafe_allow_html=True)

st.write("")

with col2:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <p class="subtext">Cadastro</p>

            <p class="text2">Aqui você poderá cadastrar clientes, fornecedores, projetos e produtos com facilidade.</p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <p class="subtext">Dados</p>

            <p class="text2">Acesso simples e rápido aos dados cadastrados, contando também com a função de exclusão</p>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <p class="subtext">Financeiro</p>

            <p class="text2">Dashboards e analitics dos dados cadastrados na base</p>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <p class="subtext">Alterar</p>

            <p class="text2">Edite facilmente dados previamente cadastrados no banco</p>
        """, unsafe_allow_html=True)