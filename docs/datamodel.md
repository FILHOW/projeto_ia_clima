# Modelagem de Dados: Previsão de Precipitação

Este documento descreve a modelagem de dados do projeto de previsão de precipitação, seguindo a arquitetura em três camadas: **System of Record (SOR)**, **System of Truth (SOT)** e **Specification (SPEC)**.

## 1. System of Record (SOR)
As tabelas nesta camada representam os dados brutos, exatamente como chegam dos arquivos `.csv`. É a primeira camada de armazenamento, garantindo que tenhamos uma cópia fiel dos dados originais.

### Tabelas: 
- `sor_weather_station_locations`
- `sor_summary_of_weather`

### Propósito:
Ingestão e arquivamento dos dados brutos sem qualquer transformação.

### Estrutura:
As colunas e os tipos de dados são uma correspondência direta dos arquivos `.csv`.

| Coluna              | Tabela                      | Tipo de Dado | Descrição                        |
|---------------------|-----------------------------|--------------|----------------------------------|
| WBAN                | sor_weather_station_locations | INT          | ID único da estação meteorológica. |
| STATE/COUNTRY ID    | sor_weather_station_locations | TEXT         | Estado/País da estação.           |

| STA                 | sor_summary_of_weather       | INT          | ID da estação.                    |
| Precip              | sor_summary_of_weather       | REAL         | Volume de precipitação.           |

### Exportar para as Planilhas

---

## 2. System of Truth (SOT)
Esta camada representa a "versão única da verdade". Os dados das tabelas SOR são limpos, padronizados e enriquecidos, servindo como a fonte confiável para análises.

### Tabela:
- `sot_clima`

### Propósito:
Fornecer dados limpos e consistentes.

### Transformações Aplicadas:
- Unificação das duas tabelas SOR (JOIN).
- Renomeação das colunas para nomes mais claros (`numero_estMeteorologica`, `nome_estado_cidade`, `numero_preciptacao`).
- Limpeza da coluna `numero_preciptacao`, tratando valores nulos e substituindo "T" por 0.0.

| Coluna               | Tipo de Dado | Descrição                                      |
|----------------------|--------------|------------------------------------------------|
| numero_estMeteorologica | INT          | ID da estação meteorológica.                  |
| nome_estado_cidade   | TEXT         | Localização da estação.                       |
| numero_preciptacao   | REAL         | Volume de precipitação (variável alvo), com valores limpos. |

### Exportar para as Planilhas

---

## 3. Specification (SPEC)
Esta é a tabela final, pronta para ser consumida pelo modelo de Machine Learning. Ela contém as features (variáveis independentes) e a variável alvo, com todas as transformações necessárias para o modelo.

### Tabela:
- `spec_clima`

### Propósito:
Fornecer um conjunto de dados de treino limpo e pronto para a modelagem.

### Estrutura:
A tabela é criada a partir da `sot_clima`, onde a coluna `nome_estado_cidade` é convertida em várias colunas numéricas binárias (uma para cada estado/cidade) usando One-Hot Encoding. Essa separação entre SOT e SPEC é crucial para garantir que a SOT permaneça consistente e a SPEC possa ser otimizada para diferentes modelos.

| Coluna                   | Tipo de Dado | Descrição                                                         |
|--------------------------|--------------|-------------------------------------------------------------------|
| numero_estMeteorologica   | INT          | ID da estação meteorológica.                                     |
| numero_preciptacao        | REAL         | Variável alvo (vendas), pronta para o modelo.                    |
| nome_estado_cidade_XX     | BOOLEAN      | Colunas criadas pelo One-Hot Encoding, indicando a localização da estação. |
