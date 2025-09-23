# clima_mvp/app/app.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from core.modelo_clima import criar_banco_de_dados_e_tabelas, inserir_dados_nas_tabelas, treinar_modelo, carregar_modelo_e_prever, dropar_banco_de_dados

st.set_page_config(page_title="Previsão de Precipitação", page_icon="🌧️", layout="wide")
st.title("🌧️ Previsão de Precipitação")
st.markdown("""
    Este aplicativo executa um **pipeline de dados completo** para um projeto de machine learning.
    O objetivo é treinar um **modelo de Regressão Linear** para prever a precipitação.
""")

st.sidebar.header("⚙️ Controle de Pipeline")
btn_criar_db = st.sidebar.button("1. Criar e Popular o Banco")
btn_dropar_db = st.sidebar.button("3. Excluir o Banco de Dados")

st.sidebar.markdown("---")
st.sidebar.subheader("Opção de Modelo")
model_option = st.sidebar.radio("Escolha a ação para o modelo:", ("Treinar Modelo", "Usar Modelo Salvo"))
btn_executar_modelo = st.sidebar.button("2. Executar Ação do Modelo")

if btn_criar_db:
    with st.spinner('Criando banco de dados e inserindo dados...'):
        sucesso_criar, msg_criar = criar_banco_de_dados_e_tabelas()
        if sucesso_criar:
            st.success(msg_criar)
            sucesso_inserir, msg_inserir = inserir_dados_nas_tabelas()
            if sucesso_inserir:
                st.success(msg_inserir)
            else:
                st.error(msg_inserir)
        else:
            st.error(msg_criar)

if btn_executar_modelo:
    with st.spinner('Executando a ação do modelo...'):
        if model_option == "Treinar Modelo":
            sucesso_modelo, modelo, metricas, coef_df, msg = treinar_modelo()
        else:
            sucesso_modelo, modelo, metricas, coef_df, msg = carregar_modelo_e_prever()

        if sucesso_modelo:
            st.success(msg)
            
            st.header("📈 Resultados da Análise")
            st.markdown("""
                As métricas a seguir avaliam o desempenho do modelo em prever a precipitação:
                * **MAE (Erro Absoluto Médio):** A média da diferença absoluta entre as previsões e os valores reais. Quanto menor, melhor.
                * **MSE (Erro Quadrático Médio):** A média do quadrado das diferenças. Puni os erros maiores, sendo mais sensível a outliers.
                * **RMSE (Raiz do Erro Quadrático Médio):** A raiz quadrada do MSE, na mesma unidade da variável de destino. Facilita a interpretação.
                * **R-quadrado (R²):** Indica a proporção da variabilidade da variável de destino que é explicada pelo modelo. Um valor mais próximo de 1 indica que o modelo se ajusta bem aos dados.
            """)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("MAE", f"**{metricas['MAE']:.2f}**")
            with col2:
                st.metric("MSE", f"**{metricas['MSE']:.2f}**")
            with col3:
                st.metric("RMSE", f"**{metricas['RMSE']:.2f}**")
            with col4:
                st.metric("R-quadrado", f"**{metricas['R2']:.2%}**")

            st.subheader("📚 Coeficientes do Modelo (Importância das Variáveis)")
            st.markdown("""
                Os coeficientes indicam o "peso" de cada variável na previsão da precipitação.
                * **Valores positivos:** Aumento na variável corresponde a um aumento na precipitação prevista.
                * **Valores negativos:** Aumento na variável corresponde a uma diminuição na precipitação prevista.
                * **Magnitude:** O valor absoluto do coeficiente indica a força do impacto na previsão.
            """)
            st.dataframe(coef_df, use_container_width=True)
        else:
            st.error(f"Erro ao executar a ação do modelo: {msg}")

if btn_dropar_db:
    sucesso_drop, msg_drop = dropar_banco_de_dados()
    if sucesso_drop:
        st.success(msg_drop)
    else:
        st.warning(msg_drop)