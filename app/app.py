import streamlit as st
import sys
import os
import pandas as pd

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import modelo_clima
from core.chatbot.rules import answer_clima_questions

st.set_page_config(layout="wide")
st.title("🌧️ Previsão de Precipitação")

st.markdown("""
    Este aplicativo executa um pipeline de Machine Learning de ponta a ponta para prever a precipitação.
    Siga os passos na barra lateral para criar o banco de dados, treinar o modelo e fazer previsões.
""")

st.sidebar.title("Passos do Pipeline")
st.sidebar.markdown("""
    Siga a ordem dos botões para executar o projeto.
""")

# Botão para criar e popular o banco de dados
if st.sidebar.button('1. Criar e Popular o Banco', help='Cria as tabelas SQL e insere os dados das tabelas SOR para SOT e SPEC.', key='create_db'):
    with st.spinner('Criando banco de dados e inserindo dados...'):
        sucesso, mensagem = modelo_clima.criar_banco_de_dados_e_tabelas()
        st.write(mensagem)
        if sucesso:
            sucesso_pop, mensagem_pop = modelo_clima.inserir_dados_nas_tabelas()
            st.write(mensagem_pop)

# Botão para treinar o modelo
if st.sidebar.button('2. Treinar o Modelo', help='Treina um modelo de Regressão Linear com os dados da tabela SPEC.', key='train_model'):
    with st.spinner('Treinando o modelo...'):
        sucesso, modelo, metricas, coef_df, mensagem = modelo_clima.treinar_modelo()
        st.write(mensagem)
        if sucesso:
            st.session_state['metrics'] = metricas
            st.session_state['coef_df'] = coef_df
            st.subheader("Métricas de Desempenho do Modelo")
            st.json(metricas)
            st.subheader("Coeficientes do Modelo")
            st.dataframe(coef_df)

# Botão para usar o modelo salvo
if st.sidebar.button('3. Usar o Modelo Salvo', help='Carrega o modelo salvo para fazer predições.', key='use_saved_model'):
    with st.spinner('Carregando modelo e fazendo previsões...'):
        sucesso, modelo, metricas, coef_df, mensagem = modelo_clima.carregar_modelo_e_prever()
        st.write(mensagem)
        if sucesso:
            st.session_state['metrics'] = metricas
            st.session_state['coef_df'] = coef_df
            st.subheader("Métricas de Desempenho do Modelo (Conjunto Completo)")
            st.json(metricas)
            st.subheader("Coeficientes do Modelo")
            st.dataframe(coef_df)
        
# Botão para dropar o banco de dados
if st.sidebar.button('4. Excluir o Banco de Dados', help='Remove o arquivo do banco de dados para iniciar o processo do zero.', key='drop_db'):
    with st.spinner('Excluindo o banco de dados...'):
        sucesso, mensagem = modelo_clima.dropar_banco_de_dados()
        st.write(mensagem)

# --- Seção do Chatbot ---
st.markdown("---")
st.subheader("🤖 Chatbot de Análise do Modelo")

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Obtém as métricas e coeficientes do estado da sessão
metrics = st.session_state.get('metrics', {})
coef_df = st.session_state.get('coef_df', pd.DataFrame())

# Lida com a entrada do usuário
if prompt := st.chat_input("Pergunte sobre as variáveis ou métricas...", key='chat_input'):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do chatbot
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = answer_clima_questions(prompt, metrics, coef_df)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})