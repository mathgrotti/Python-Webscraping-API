import pdfplumber
import pandas as pd
import zipfile
import os
from tqdm import tqdm
import numpy as np
import csv

def extrair_tabelas(pdf_path):
    """Extrai tabelas de todas as páginas com estruturação aprimorada"""
    tabelas = []
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in tqdm(pdf.pages, desc="Processando páginas"):
            try:
                # Extrai a tabela com configurações otimizadas
                tabela = pagina.extract_table({
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "intersection_tolerance": 20,
                    "intersection_x_tolerance": 15,
                    "intersection_y_tolerance": 15,
                    "snap_tolerance": 8
                })
                
                if tabela and len(tabela) > 1:
                    # Processa cada célula da tabela
                    tabela_processada = []
                    for linha in tabela:
                        linha_processada = [
                            str(celula).strip() if celula is not None and str(celula).strip() != "" else None
                            for celula in linha
                        ]
                        if any(celula is not None for celula in linha_processada):
                            tabela_processada.append(linha_processada)
                    
                    if len(tabela_processada) > 1:  # Pelo menos cabeçalho + uma linha de dados
                        tabelas.append(tabela_processada)
                        
            except Exception as e:
                print(f"\nErro na página {pagina.page_number}: {str(e)}")
                continue
    
    return tabelas

def processar_dados(tabelas):
    """Processa e consolida todas as tabelas mantendo a estrutura"""
    if not tabelas:
        return pd.DataFrame()
    
    # Lista para armazenar todos os DataFrames
    dfs = []
    
    for i, tabela in enumerate(tabelas):
        try:
            if not tabela or len(tabela) < 2:
                continue
                
            # Processa cabeçalhos
            cabecalhos = []
            contador = {}
            for original in tabela[0]:
                # Limpa e padroniza o cabeçalho
                cabecalho = str(original).strip() if original is not None else ""
                cabecalho = cabecalho if cabecalho else f"Coluna_{len(cabecalhos)}"
                
                # Trata cabeçalhos duplicados
                if cabecalho in contador:
                    contador[cabecalho] += 1
                    cabecalho_final = f"{cabecalho}_{contador[cabecalho]}"
                else:
                    contador[cabecalho] = 0
                    cabecalho_final = cabecalho
                
                cabecalhos.append(cabecalho_final)
            
            # Cria DataFrame
            dados = tabela[1:]  # Remove a linha de cabeçalho
            df = pd.DataFrame(dados, columns=cabecalhos)
            
            # Remove linhas totalmente vazias
            df = df.replace('', np.nan)
            df = df.dropna(how='all')
            
            if not df.empty:
                dfs.append(df)
                
        except Exception as e:
            print(f"\nErro ao processar tabela {i}: {str(e)}")
            continue
    
    # Consolida todos os DataFrames
    if not dfs:
        return pd.DataFrame()
    
    try:
        # Encontra todas as colunas únicas
        todas_colunas = set()
        for df in dfs:
            todas_colunas.update(df.columns)
        
        # Cria um DataFrame consolidado
        df_final = pd.DataFrame(columns=list(todas_colunas))
        
        for df in dfs:
            # Adiciona colunas faltantes
            for col in todas_colunas:
                if col not in df.columns:
                    df[col] = None
            
            # Reordena colunas e concatena
            df = df[list(todas_colunas)]
            df_final = pd.concat([df_final, df], ignore_index=True)
        
        return df_final
    
    except Exception as e:
        print(f"\nErro ao consolidar tabelas: {str(e)}")
        return pd.DataFrame()

def salvar_resultados(df, saida_csv, saida_zip):
    """Salva os dados em CSV e ZIP com formatação adequada"""
    if df.empty:
        print("Nenhum dado válido para salvar.")
        return False
    
    try:
        # Garante que o diretório de saída existe
        os.makedirs('../data/processed', exist_ok=True)
        
        # Padroniza colunas importantes
        colunas_priorizadas = ['PROCEDIMENTO', 'CODIGO', 'DESCRICAO', 'OD', 'AMB', 'PORTE', 'UF']
        
        # Reorganiza colunas (mantém as priorizadas primeiro)
        colunas_ordenadas = (
            [col for col in colunas_priorizadas if col in df.columns] +
            [col for col in df.columns if col not in colunas_priorizadas]
        )
        
        df = df[colunas_ordenadas]
        
        # Aplica transformações específicas
        mapeamento = {
            'OD': {'S': 'Seguro Saúde', 'N': 'Não'},
            'AMB': {'S': 'Ambulatorial', 'N': 'Não'}
        }
        
        for col, map_val in mapeamento.items():
            if col in df.columns:
                df[col] = df[col].replace(map_val)
        
        # Caminhos dos arquivos
        caminho_csv = os.path.join('../../data/processed', saida_csv)
        caminho_zip = os.path.join('../../data/processed', saida_zip)
        
        # Salva CSV com formatação adequada
        df.to_csv(
            caminho_csv,
            index=False,
            encoding='utf-8-sig',
            quoting=csv.QUOTE_MINIMAL,
            quotechar='"',
            sep=','
        )
        
        # Cria arquivo ZIP
        with zipfile.ZipFile(caminho_zip, 'w') as zipf:
            zipf.write(caminho_csv, os.path.basename(caminho_csv))
        
        print(f"\n✅ Arquivos salvos com sucesso:")
        print(f"- CSV: {caminho_csv}")
        print(f"- ZIP: {caminho_zip}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Erro ao salvar resultados: {str(e)}")
        return False

if __name__ == "__main__":
    # Configurações
    PDF_PATH = "../../data/raw/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    CSV_OUTPUT = "rol_procedimentos.csv"
    ZIP_OUTPUT = "Teste_Matheus_Grotti.zip"
    
    print("Iniciando processamento do PDF...")
    
    # Extrai tabelas de todas as páginas
    tabelas = extrair_tabelas(PDF_PATH)
    
    if not tabelas:
        print("\n⚠️ Nenhuma tabela foi encontrada no documento.")
        print("Possíveis causas:")
        print("- O PDF não contém tabelas reconhecíveis")
        print("- O arquivo pode estar protegido ou corrompido")
        print("- A estrutura do PDF é muito complexa")
        exit(1)
    
    print(f"\n✅ {len(tabelas)} tabelas extraídas com sucesso.")
    
    # Processa e consolida os dados
    df_final = processar_dados(tabelas)
    
    if df_final.empty:
        print("\n⚠️ Nenhum dado válido foi processado.")
        exit(1)
    
    print(f"\nDados processados: {len(df_final)} linhas encontradas.")
    
    # Salva os resultados
    if not salvar_resultados(df_final, CSV_OUTPUT, ZIP_OUTPUT):
        exit(1)