import os
import pandas as pd
from pathlib import Path  # Recomendado para manipulação de caminhos

def carregar_dados_csv():
    csv_path = Path(__file__).parent.parent.parent / 'data' / 'Relatorio_cadop.csv'
    return pd.read_csv(csv_path, sep=';', encoding='utf-8')  # Volta 2 níveis e entra em data/

    # Verifica se o arquivo existe
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado em: {csv_path}")

    # Carrega com tratamento de erros
    try:
        df = pd.read_csv(
            csv_path,
            sep=";",
            encoding="utf-8",
            dtype=str,
            na_values=["", "NA", "N/A", "NaN"],
            keep_default_na=False
        )
        
        # Limpeza básica dos dados
        text_cols = df.select_dtypes(include=['object']).columns
        df[text_cols] = df[text_cols].apply(
            lambda col: col.str.replace(r'\r\n|\n|\r', ' ', regex=True)  # Remove quebras de linha
                      .str.strip()  # Remove espaços extras
        )
        
        return df
        
    except Exception as e:
        raise Exception(f"Erro ao carregar CSV: {str(e)}")