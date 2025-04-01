use ans_operadoras;

SELECT 
    d.registro_ans,
    o.razao_social AS nome_operadora,
    COUNT(*) AS registros,
    SUM(d.despesa) AS total_despesas,
    ROUND(SUM(d.despesa) / 1000000, 2) AS despesas_milhoes
FROM 
    demonstrativos_contabeis d
JOIN 
    operadoras_ativas o ON d.registro_ans = o.registro_ans
WHERE 
    d.ano = 2024
    AND d.nome_operadora LIKE '%EVENTOS/%SINISTROS%'
GROUP BY 
    d.registro_ans, o.razao_social
ORDER BY 
    total_despesas DESC
LIMIT 10;