from fastapi import APIRouter, HTTPException, Query
from ..utils.csv_loader import carregar_dados_csv
import pandas as pd
import numpy as np

router = APIRouter()

def clean_data(df):
    # Substitui infinitos e NaNs por None (que vira null no JSON)
    df = df.replace([np.inf, -np.inf], np.nan)
    return df.where(pd.notnull(df), None)

@router.get("/operadoras")
async def buscar_operadoras(termo: str = Query(None)):
    try:
        df = carregar_dados_csv()
        df = clean_data(df)  # Limpa os dados
        
        if termo:
            termo = termo.lower()
            cols = ['Nome_Fantasia', 'Razao_Social', 'Registro_ANS', 'CNPJ']
            mask = df[cols].apply(
                lambda col: col.astype(str).str.lower().str.contains(termo)
            ).any(axis=1)
            resultados = df[mask]
        else:
            resultados = df.head(50)
            
        # Converte para dict tratando os valores problemáticos
        return {
            "operadoras": resultados.apply(
                lambda x: x.where(pd.notnull(x), None).astype(object)
            ).to_dict(orient='records')
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar busca: {str(e)}"
        )