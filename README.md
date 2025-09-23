# Pipeline de Previsão de Precipitação

MVP educacional para o projeto de previsão de precipitação, com treino de um modelo de regressão e documentação organizada.

## 📖 Documentação

A documentação completa está na pasta `docs/`:

- PMC
- Arquitetura
- Modelagem de Dados
- Governança LGPD/DAMA
- Testes
- Deploy

## 🖥️ Como rodar o projeto no Visual Studio Code ou no Terminal

### 1. Abrir o projeto

- Abra o **VS Code**.
- Vá em **File → Open Folder** e escolha a pasta do seu projeto, `clima_mvp/`.

### 2. Criar e ativar ambiente virtual

No terminal integrado do VS Code (`Ctrl+`):

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar no Linux/Mac
source .venv/bin/activate

# Ativar no Windows (PowerShell)
.venv\Scripts\Activate.ps1
```
> ⚠️ No canto inferior direito do VS Code, selecione o interpretador Python da pasta .venv.

### 3. Instalar dependências
Com o ambiente ativo:

```bash
pip install -r requirements.txt
```

### 4. Rodar o Streamlit
No seu terminal ou CMD, navegue até a pasta raiz do projeto e execute o comando a seguir:

```bash
streamlit run app/app.py
```

O aplicativo abrirá no seu navegador padrão em http://localhost:8501.

### 5. Trabalhar com o código
- **Front-end**: app/app.py (UI em Streamlit).

- **Back-end**: core/ (dados, modelos e lógica do pipeline).

- **Notebooks**: notebooks/01_eda_clima.ipynb (exploração inicial dos dados).

### 6. Rodar testes

```bash
pytest tests/
```
## 📂 Estrutura de pastas

```bash
clima_mvp/
├─ app/            # Interface com o usuário (Streamlit)
├─ core/           # Lógica de negócio (dados, modelos)
│   ├── data/      # Dados brutos, scripts SQL e banco de dados gerado
│   └── modelo_clima.py
├─ models/         # Modelo treinado salvo (.pickle)
├─ docs/           # Documentação (PMC, arquitetura, etc.)
├─ notebooks/      # Notebooks de exploração (EDA)
├─ requirements.txt
└─ README.md
```

---

## 🚀 Deploy
Para publicar rapidamente, veja a documentação na pasta [docs/deployment.md](./docs/deployment.md).
