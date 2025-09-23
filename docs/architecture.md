# Arquitetura da Aplicação - Previsão de Precipitação

Este documento descreve a arquitetura e o fluxo de dados da aplicação Streamlit para análise e previsão de precipitação.

## Fluxo de Dados e Processamento
O fluxo foi desenhado para ser modular e robusto, separando a ingestão, o tratamento e a modelagem dos dados.

### Ingestão de Dados (Backend):
Ao clicar em "Criar e Popular o Banco", a aplicação lê os arquivos de dados brutos (`Weather Station Locations.csv` e `Summary of Weather.csv`) que já estão localizados na pasta `core/data/`.

### Criação do Banco de Dados (Backend):
O pipeline cria um banco de dados SQLite (`clima_database.db`) do zero. As tabelas `sor_weather_station_locations`, `sor_summary_of_weather`, `sot_clima` e `spec_clima` são criadas a partir dos scripts SQL localizados em `core/data/`.

### Pipeline ETL (Extract, Transform, Load):

- **E (Extract)**: O conteúdo dos arquivos `.csv` é lido em DataFrames do pandas.

- **T (Transform) & L (Load)**:
  - **SOR**: Os dados brutos são inseridos nas tabelas `sor_weather_station_locations` e `sor_summary_of_weather`.
  - **SOT**: Os dados das tabelas SOR são unificados (JOIN) e um processo de limpeza e transformação é aplicado (tratamento de valores T e nulos na coluna de precipitação). O resultado limpo é salvo na `sot_clima`.
  - **SPEC**: Os dados da SOT são carregados na `spec_clima`, que serve como a fonte final para o treinamento do modelo. Nesta etapa, a coluna `nome_estado_cidade` é transformada em colunas numéricas (One-Hot Encoding).

### Treinamento do Modelo (Machine Learning):

- Os dados são lidos da tabela `spec_clima`.
- O conjunto de dados é dividido em features (X) e alvo (y).
- Um modelo de Regressão Linear é treinado (`modelo_clima.py`).

### Armazenamento do Modelo (Serialização):
Após o treinamento, o objeto do modelo é serializado usando pickle. O modelo é salvo como `modelo_clima.pickle` dentro da pasta `models/`.

### Apresentação de Resultados (UI):
As métricas de avaliação do modelo (como MAE, MSE, RMSE e R²) e a importância das features (coeficientes) são calculadas. Os resultados são exibidos na interface do Streamlit.

### Limpeza (Cleanup):
O usuário pode clicar no botão "Excluir o Banco de Dados" para remover o arquivo `clima_database.db`, o que permite reiniciar o estado da aplicação para uma nova execução.
