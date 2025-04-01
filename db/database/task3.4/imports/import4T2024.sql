LOAD DATA INFILE '/var/lib/mysql-files/4T2024.csv'
INTO TABLE demonstrativos_contabeis
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS  -- Ignora cabeçalho
(@data, @registro_ans, @conta_contabil, @descricao, @saldo_inicial, @saldo_final)
SET
    registro_ans = NULLIF(@registro_ans, ''),
    -- Extrai CNPJ da descrição
    cnpj = IF(@descricao REGEXP '[0-9]{2}\\.[0-9]{3}\\.[0-9]{3}/[0-9]{4}-[0-9]{2}', 
             REGEXP_SUBSTR(@descricao, '[0-9]{2}\\.[0-9]{3}\\.[0-9]{3}/[0-9]{4}-[0-9]{2}'),
             NULL),
    ano = YEAR(STR_TO_DATE(@data, '%Y-%m-%d')),
    nome_operadora = NULLIF(@descricao, ''),
    -- Converte formato brasileiro (1.234,56 → 1234.56)
    receita = IFNULL(CAST(REPLACE(REPLACE(@saldo_final, '.', ''), ',', '.') AS DECIMAL(15,2)), 0),
    despesa = IFNULL(CAST(REPLACE(REPLACE(@saldo_inicial, '.', ''), ',', '.') AS DECIMAL(15,2)), 0),
    lucro = IFNULL(CAST(REPLACE(REPLACE(@saldo_final, '.', ''), ',', '.') AS DECIMAL(15,2)) - 
                CAST(REPLACE(REPLACE(@saldo_inicial, '.', ''), ',', '.') AS DECIMAL(15,2)), 0),
	trimestre = 4;