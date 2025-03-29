CREATE DATABASE IF NOT EXISTS ans_operadoras;
USE ans_operadoras;

-- Tabela de operadoras
CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(100),
    representante VARCHAR(100),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE
);

-- Tabela de demonstrações contábeis
CREATE TABLE IF NOT EXISTS demonstracoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(20),
    ano INT,
    trimestre INT,
    conta VARCHAR(255),
    valor DECIMAL(15, 2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);

-- database/import.sql
-- Importação dos dados

-- Importar operadoras (ajuste o caminho do arquivo)
LOAD DATA INFILE '/path/to/Operadoras_ativas.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, 
numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, 
email, representante, cargo_representante, @data_registro_ans)
SET data_registro_ans = STR_TO_DATE(@data_registro_ans, '%d/%m/%Y');

-- Importar demonstrações contábeis (ajuste conforme seus arquivos)
-- Você precisará processar os arquivos ZIP/CSV primeiro