# clima_mvp/core/modelo_clima.py
import pandas as pd
import numpy as np
import sqlite3
import os
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

DATABASE_NAME = 'clima_database.db'
DATABASE_PATH = os.path.join('core', 'data', DATABASE_NAME)
SQL_PATH = os.path.join('core', 'data')
MODEL_PATH = os.path.join('models', 'modelo_clima.pickle')

def criar_banco_de_dados_e_tabelas():
    """
    Cria o banco de dados SQLite e as tabelas com base nos arquivos SQL.
    Se o banco de dados já existir, ele é removido e recriado.
    """
    try:
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        sql_files = ['sor_weather_station_locations.sql', 'sor_summary_of_weather.sql',
                     'sot_clima.sql', 'spec_clima.sql']
        
        for file in sql_files:
            with open(os.path.join(SQL_PATH, file), 'r') as f:
                sql_script = f.read()
                cursor.executescript(sql_script)

        conn.commit()
        conn.close()
        return True, "Banco de dados e tabelas criados com sucesso!"
    except Exception as e:
        return False, f"Erro ao criar o banco de dados e tabelas: {e}"

def inserir_dados_nas_tabelas():
    """Insere os dados dos CSVs nas tabelas SOR, depois o tratamento na SOT e SPEC."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Carregar e filtrar dados dos CSVs para as tabelas SOR
        df_sor1 = pd.read_csv(os.path.join('data', 'Weather Station Locations.csv'))
        df_sor2 = pd.read_csv(os.path.join('data', 'Summary of Weather.csv'), low_memory=False)

        cols_sor1 = ['WBAN', 'STATE/COUNTRY ID']
        df_sor1_filtered = df_sor1[cols_sor1]

        cols_sor2 = ['STA', 'Precip']
        df_sor2_filtered = df_sor2[cols_sor2]

        df_sor1_filtered.to_sql('sor_weather_station_locations', conn, if_exists='append', index=False)
        df_sor2_filtered.to_sql('sor_summary_of_weather', conn, if_exists='append', index=False)

        # ETL para SOT
        df_merged = pd.merge(df_sor1, df_sor2, left_on='WBAN', right_on='STA', how='inner')
        df_merged = df_merged.rename(columns={
            'WBAN': 'numero_estMeteorologica',
            'STATE/COUNTRY ID': 'nome_estado_cidade',
            'Precip': 'numero_preciptacao'
        })
        
        cols_sot = ['numero_estMeteorologica', 'nome_estado_cidade', 'numero_preciptacao']
        df_sot = df_merged[cols_sot]
        df_sot['numero_preciptacao'] = df_sot['numero_preciptacao'].replace('T', 0.0).astype(float)
        df_sot.dropna(subset=['numero_preciptacao'], inplace=True)
        df_sot.to_sql('sot_clima', conn, if_exists='append', index=False)

        # ETL para SPEC
        df_spec = pd.get_dummies(df_sot, columns=['nome_estado_cidade'], prefix='nome_estado_cidade', dtype=int)
        
        spec_cols = [col for col in df_spec.columns if col.startswith('numero') or col.startswith('nome_estado_cidade')]
        df_spec[spec_cols].to_sql('spec_clima', conn, if_exists='append', index=False)

        conn.close()
        return True, "Dados inseridos com sucesso nas tabelas SOR, SOT e SPEC!"
    except Exception as e:
        return False, f"Erro ao inserir dados: {e}"

def treinar_modelo():
    """
    Carrega dados da SPEC, treina o modelo de regressão,
    salva o modelo e retorna os resultados e uma mensagem de sucesso.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        df_spec = pd.read_sql_query("SELECT * FROM spec_clima", conn)
        conn.close()

        features = [col for col in df_spec.columns if col not in ['index', 'numero_estMeteorologica', 'numero_preciptacao']]
        X = df_spec[features]
        y = df_spec['numero_preciptacao']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        model_path = os.path.join('models', 'modelo_clima.pickle')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        metrics = {
            'MAE': mean_absolute_error(y_test, y_pred),
            'MSE': mean_squared_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'R2': r2_score(y_test, y_pred)
        }
        
        coef_df = pd.DataFrame({'Variável': X.columns, 'Coeficiente': model.coef_})
        
        return True, model, metrics, coef_df, f"✅ Modelo treinado e salvo com sucesso em: {model_path}"
    except Exception as e:
        return False, None, None, None, f"Erro ao treinar ou salvar o modelo: {e}"

def carregar_modelo_e_prever():
    """
    Carrega o modelo salvo, faz a predição na tabela SPEC e retorna os resultados.
    """
    if not os.path.exists(MODEL_PATH):
        return False, None, None, None, "❌ Erro: O arquivo do modelo não foi encontrado. Por favor, treine e salve o modelo primeiro."

    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        conn = sqlite3.connect(DATABASE_PATH)
        df_spec = pd.read_sql_query("SELECT * FROM spec_clima", conn)
        conn.close()

        features = [col for col in df_spec.columns if col not in ['index', 'numero_estMeteorologica', 'numero_preciptacao']]
        X = df_spec[features]
        y = df_spec['numero_preciptacao']
        
        y_pred = model.predict(X)
        
        metrics = {
            'MAE': mean_absolute_error(y, y_pred),
            'MSE': mean_squared_error(y, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y, y_pred)),
            'R2': r2_score(y, y_pred)
        }
        
        coef_df = pd.DataFrame({'Variável': X.columns, 'Coeficiente': model.coef_})

        return True, model, metrics, coef_df, f"✅ Modelo carregado com sucesso e predição realizada!"

    except Exception as e:
        return False, None, None, None, f"Erro ao carregar o modelo ou fazer predição: {e}"


def dropar_banco_de_dados():
    """Remove o arquivo do banco de dados para limpar o ambiente."""
    try:
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
            return True, "Banco de dados removido com sucesso."
        return False, "O arquivo do banco de dados não existe."
    except Exception as e:
        return False, f"Erro ao remover o banco de dados: {e}"