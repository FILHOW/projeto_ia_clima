# Project Model Canvas — Pipeline de Previsão de Precipitação (Clima)

## Contexto:
A previsão de eventos climáticos como a precipitação é vital para diversos setores, como agricultura, logística e gestão de recursos hídricos. O projeto utiliza um conjunto de dados detalhado sobre estações meteorológicas e registros de clima. O objetivo é criar um pipeline de Machine Learning que preveja o volume de chuva com base em características das estações e do tempo.

## Problema a ser Respondido:
Como as características de uma estação meteorológica (localização, etc.) influenciam o volume de precipitação? É possível prever a precipitação futura de um local com um bom nível de acerto?

## Pergunta Norteadora:
Quais características mais impactam a precipitação (numero_preciptacao)? Podemos treinar um modelo de Regressão Linear que forneça previsões úteis para a tomada de decisão?

## Solução Proposta:
Desenvolver uma aplicação interativa em Streamlit que:

- Permita a ingestão e o pré-processamento dos arquivos de dados brutos (.csv).
- Treine um modelo de Regressão Linear para prever a numero_preciptacao.
- Mostre métricas de avaliação claras do modelo (MAE, MSE, RMSE e R²).
- Explique a importância das variáveis por meio dos coeficientes do modelo.
- Permita carregar um modelo já treinado e salvo para fazer novas previsões rapidamente.

## Desenho de Arquitetura:
O sistema é estruturado em camadas para garantir organização e manutenibilidade:

- **Interface (app/)**: Streamlit como front-end para a execução do pipeline e visualização de resultados.
- **Core (core/)**: Módulos para o pipeline de dados, pré-processamento, treino de modelos e avaliação.
- **Dados (core/data/)**: Pastas para os arquivos de dados brutos (.csv), scripts SQL para a criação das tabelas (SOR, SOT, SPEC) e o banco de dados SQLite.
- **Modelo (models/)**: Pasta para armazenar o modelo treinado em um arquivo .pickle.
