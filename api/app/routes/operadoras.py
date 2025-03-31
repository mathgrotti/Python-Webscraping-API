from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import numpy as np
from pathlib import Path
import json
import os

router = APIRouter()

def safe_convert(value):
    """Converte valores problemáticos para None"""
    if pd.isna(value) or value in [np.inf, -np.inf]:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return str(value)

@router.get("/operadoras")
async def get_operadoras(termo: str = Query(None, description="Termo para busca em nome, CNPJ ou registro")):
    try:
        csv_path = Path(__file__).parent.parent.parent / "data" / "Relatorio_cadop.csv"
        
        print(f"Caminho do CSV: {csv_path}")
        print(f"Arquivo existe? {os.path.exists(csv_path)}")
        print(f"Termo de busca recebido: {termo}")
        
        # Carrega mantendo todos como strings inicialmente
        df = pd.read_csv(
            csv_path,
            sep=";",
            encoding='utf-8',
            dtype=str,
            na_values=["", "NA", "N/A", "NaN", "NULL"],
            keep_default_na=False
        )
        
        # Aplica conversão segura para todas as colunas
        for col in df.columns:
            df[col] = df[col].apply(safe_convert)
        
        # Filtragem baseada no termo de busca
        if termo:
            # Converte termo para minúsculo para comparação case-insensitive
            termo = termo.lower()
            
            # Colunas comuns para busca
            colunas_busca = ['Registro_ANS', 'CNPJ', 'Razao_Social', 'Nome_Fantasia']
            
            # Filtro para cada coluna
            filtros = []
            for coluna in colunas_busca:
                if coluna in df.columns:
                    # Converte para string antes de aplicar lower()
                    filtros.append(df[coluna].astype(str).str.lower().str.contains(termo))
            
            # Combina os filtros com OR
            if filtros:
                mascara_filtro = filtros[0]
                for filtro in filtros[1:]:
                    mascara_filtro = mascara_filtro | filtro
                
                df = df[mascara_filtro]
                
            print(f"Encontradas {len(df)} operadoras após filtro")
        
        # Limita o número de resultados para não sobrecarregar
        resultados = df.head(100)
        
        # Conversão segura para JSON
        operadoras = json.loads(
            resultados.to_json(
                orient="records",
                force_ascii=False,
                default_handler=str
            )
        )
        
        print(f"Retornando {len(operadoras)} operadoras")
        return operadoras
        
    except Exception as e:
        print(f"ERRO: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar: {str(e)}"
        )