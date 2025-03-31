USE ans_operadoras;

CREATE TABLE IF NOT EXISTS operadoras_ativas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(20),
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2),
    municipio VARCHAR(100),
    data_registro DATE,
    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS demonstrativos_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(30) NOT NULL,
    cnpj VARCHAR(50),
    ano INT NOT NULL,
    nome_operadora VARCHAR(255) NOT NULL,
    receita DECIMAL(15,2),
    despesa DECIMAL(15,2),
    lucro DECIMAL(15,2),
    data_importacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    trimestre INT,
    INDEX idx_registro_ans (registro_ans),
    INDEX idx_ano_trimestre (ano, trimestre)
);