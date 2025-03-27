import pdfplumber
import pandas as pd
import zipfile
import os
from tqdm import tqdm

def extrair_tabelas(pdf_path):
    """Extrai todas as tabelas do PDF usando pdfplumber"""
    tabelas = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for pagina in tqdm(pdf.pages, desc="Extraindo tabelas"):
                tabelas_pagina = pagina.extract_tables({
                    "vertical_strategy": "text",
                    "horizontal_strategy": "text",
                    "snap_tolerance": 4
                })
                
                for tabela in tabelas_pagina:
                    if tabela and len(tabela) > 1:  # Ignora tabelas vazias ou só com cabeçalho
                        df = pd.DataFrame(tabela[1:], columns=tabela[0])
                        tabelas.append(df)
    except Exception as e:
        print(f"\nErro ao processar PDF: {e}")
    return tabelas

def processar_dados(tabelas):
    """Combina e limpa os dados extraídos"""
    if not tabelas:
        return pd.DataFrame()
    
    df = pd.concat(tabelas, ignore_index=True)
    
    # Limpeza básica
    df = df.dropna(how='all').drop_duplicates()
    
    # Renomear colunas (ajuste conforme seu PDF)
    if len(df.columns) >= 7:
        df.columns = ['PROCEDIMENTO', 'CODIGO', 'DESCRICAO', 'OD', 'AMB', 'PORTE', 'UF']
        
        # Substituir abreviações
        df['OD'] = df['OD'].replace({'S': 'Seguro Saúde', 'N': 'Não'})
        df['AMB'] = df['AMB'].replace({'S': 'Ambulatorial', 'N': 'Não'})
    
    return df

def salvar_resultados(df, saida_csv, saida_zip):
    """Salva os dados processados em CSV e compacta"""
    if df.empty:
        print("Nenhum dado válido para salvar.")
        return False
    
    os.makedirs('../data/processed', exist_ok=True)
    caminho_csv = os.path.join('../data/processed', saida_csv)
    caminho_zip = os.path.join('../data/processed', saida_zip)
    
    try:
        df.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
        
        with zipfile.ZipFile(caminho_zip, 'w') as zipf:
            zipf.write(caminho_csv, os.path.basename(caminho_csv))
        
        print(f"\nResultados salvos em: {caminho_zip}")
        return True
    except Exception as e:
        print(f"\nErro ao salvar resultados: {e}")
        return False

if __name__ == "__main__":
    # Configurações
    PDF_PATH = "../data/raw/Anexo_I.pdf"
    CSV_OUTPUT = "rol_procedimentos.csv"
    ZIP_OUTPUT = "Teste_Seu_Nome.zip"
    
    print("Iniciando transformação de dados...")
    
    # Processo completo
    tabelas_extraidas = extrair_tabelas(PDF_PATH)
    dados_processados = processar_dados(tabelas_extraidas)
    salvar_resultados(dados_processados, CSV_OUTPUT, ZIP_OUTPUT)