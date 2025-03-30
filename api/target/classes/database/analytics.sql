-- 10 operadoras com maiores despesas no último trimestre
SELECT o.razao_social, o.nome_fantasia, SUM(d.valor) AS total_despesas
FROM demonstracoes d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.conta LIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
AND d.ano = (SELECT MAX(ano) FROM demonstracoes)
AND d.trimestre = (SELECT MAX(trimestre) FROM demonstracoes WHERE ano = (SELECT MAX(ano) FROM demonstracoes))
GROUP BY o.razao_social, o.nome_fantasia
ORDER BY total_despesas DESC
LIMIT 10;

-- 10 operadoras com maiores despesas no último ano
SELECT o.razao_social, o.nome_fantasia, SUM(d.valor) AS total_despesas
FROM demonstracoes d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.conta LIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
AND d.ano = (SELECT MAX(ano) FROM demonstracoes)
GROUP BY o.razao_social, o.nome_fantasia
ORDER BY total_despesas DESC
LIMIT 10;