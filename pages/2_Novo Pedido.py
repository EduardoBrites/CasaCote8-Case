import streamlit as st

st.set_page_config(
    page_title="CasaCote8 - Novo Pedido", 
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