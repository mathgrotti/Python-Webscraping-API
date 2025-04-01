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