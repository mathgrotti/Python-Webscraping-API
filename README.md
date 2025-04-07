# 🩺 Webscraper + API ANS

📌 O que é <br>
Sistema completo que automatiza a coleta, transformação, armazenamento e exibição de dados públicos da ANS (Agência Nacional de Saúde Suplementar). A solução entrega uma API REST robusta e um frontend leve para consultar operadoras de saúde.

💡 Por que criei <br>
A ANS disponibiliza dados valiosos, mas de forma pouco amigável — espalhados em PDFs e com acesso manual. Resolvi transformar essa realidade com um sistema que automatiza esse processo de ponta a ponta. A ideia nasceu da curiosidade e virou um laboratório prático para testar habilidades em scraping, backend, SQL e Docker, tudo com propósito real.

🛠️ Tecnologias usadas

Python (BeautifulSoup, Selenium, FastAPI)

MySQL

Docker & Docker Compose

Vue.js (frontend)

Pandas, PyPDF2

Node.js
<br><br>


Primeiramente, dentro de Python-Webscraping-API execute o comando para instalar todas as dependências necessárias:

    pip install -r requirements.txt

## 1. Webscraping

O componente de webscraping é responsável por extrair dados do site da ANS.

### Funcionalidades

-   Coleta automatizada de informações sobre operadoras de saúde
-   Armazenamento dos dados brutos para processamento posterior

### Tecnologias

-   Python
-   Bibliotecas de scraping (BeautifulSoup/Selenium)
-   Localizado em:  web_scraping

#### Como usar

    cd webscraping/web_scraping
    python3 download_anexos.py

## 2. PDF para CSV

Módulo responsável pela transformação de dados de PDFs para formato CSV estruturado.

### Funcionalidades

-   Extração de texto de documentos PDF
-   Tratamento e estruturação dos dados
-   Exportação para formato CSV

### Implementação

O arquivo  pdf_to_csv.py  contém as funções para transformação dos dados:

    cd webscraping/data_transformation
    python3 pdf_to_csv.py

### Dados gerados

Os dados processados são armazenados em Documents/data/processed/

## 3. Banco de Dados

Sistema de armazenamento SQL para dados estruturados das operadoras.

### Configuração

- Configuração do banco via db/application.properties
- Queries do banco em db/database

### Tecnologias

-   Sistema SQL (MySQL/PostgreSQL)
-   Docker para containerização

### Execução

Para iniciar o banco de dados:

    docker-compose up -d db
## 4. API

Interface REST para consulta aos dados das operadoras de saúde.

### Endpoints principais

-   `GET /api/operadoras`: Retorna lista de operadoras

### Tecnologias

-   FastAPI
-   Python
-   Docker

### Estrutura

-   Arquivo principal:  api/app/main.py
-   Rotas:  api/app/routes
-   Utilitários:  api/app/utils

### Como executar
#### Localmente

    cd api
    uvicorn app.main:app --reload
    Acesse em: http://localhost:8000/api/operadoras
    
 #### Com Docker
    docker-compose up -d

### Frontend

Um frontend simples está disponível em  webapp  para visualização dos dados:

    cd api/webapp
    npm install
    npm run serve
Acesse em: http://localhost:5173

## Requisitos do sistema

-   Python 3.8+
-   Node.js 14+ (para o frontend)
-   Docker e Docker Compose (para containerização)

## Como iniciar o projeto completo
    # Clonar o repositório
    git clone https://github.com/mathgrotti/Python-Webscraping-API.git
    
    # Iniciar todos os serviços
    docker-compose up -d
    
    # Acessar frontend
    # http://localhost:5173
    
    # Acessar API
    # http://localhost:8000

<br><br>
### 🚀 Destaques do projeto

🕸️ Webscraping inteligente dos anexos de operadoras no site da ANS

📄 Conversão de PDFs para CSVs estruturados com limpeza e normalização dos dados

💾 Armazenamento em banco relacional com queries analíticas organizadas

🔗 API REST (FastAPI) para consulta aos dados de forma simples e eficiente

🌐 Frontend com Vue.js para visualização rápida e amigável

🧪 Ambiente completo para testes locais com docker-compose up
