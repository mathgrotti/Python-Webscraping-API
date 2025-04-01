USE ans_operadoras;

LOAD DATA INFILE '/var/lib/mysql-files/Relatorio_cadop.csv'
INTO TABLE operadoras_ativas
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@Registro_ANS, @CNPJ, @Razao_Social, @Nome_Fantasia, @Modalidade, 
 @Logradouro, @Numero, @Complemento, @Bairro, @Cidade, @UF, @CEP, 
 @DDD, @Telefone, @Fax, @Endereco_eletronico, @Representante, 
 @Cargo_Representante, @Regiao_de_Comercializacao, @Data_Registro_ANS)
SET
    registro_ans = NULLIF(@Registro_ANS, ''),
    cnpj = NULLIF(@CNPJ, ''),
    razao_social = NULLIF(@Razao_Social, ''),
    nome_fantasia = NULLIF(@Nome_Fantasia, ''),
    modalidade = NULLIF(@Modalidade, ''),
    uf = NULLIF(@UF, ''),
    municipio = CONCAT_WS(' - ', NULLIF(@Cidade, ''), NULLIF(@UF, '')),
    data_registro = NULLIF(@Data_Registro_ANS, '');
    
SELECT 
    registro_ans AS ANS,
    cnpj AS CNPJ,
    SUBSTRING(razao_social, 1, 20) AS Razao_Social,
    uf AS UF,
    data_registro AS 'Data Registro'
FROM operadoras_ativas
LIMIT 5;
    