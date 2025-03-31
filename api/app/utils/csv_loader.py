import pandas as pd
import os

def carregar_dados_csv():
    csv_path = os.path.join(os.path.dirname(__file__), "../../data/Relatorio_cadop.csv")
    
    # Especifica dtype como string para evitar conversão automática para float
    df = pd.read_csv(
        csv_path,
        sep=";",
        encoding="utf-8",
        dtype=str,  # Carrega tudo como string inicialmente
        na_values=["", "NA", "N/A", "NaN"]
    )
    
    # Converte apenas colunas numéricas explicitamente
    numeric_cols = ['Registro_ANS']  # Adicione outras colunas numéricas se necessário
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df