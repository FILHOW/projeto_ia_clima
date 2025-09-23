-- clima_mvp/core/data/sot_clima.sql

-- Tabela que armazena os dados unificados e transformados.
-- Ela é o resultado do JOIN entre as tabelas SOR.
CREATE TABLE IF NOT EXISTS sot_clima (
    numero_estMeteorologica INT NOT NULL,
    nome_estado_cidade VARCHAR(255) NOT NULL,
    numero_preciptacao FLOAT NOT NULL
);