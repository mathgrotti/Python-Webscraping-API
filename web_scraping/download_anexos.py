import requests
from bs4 import BeautifulSoup
import os
import zipfile

def baixar_pdf(url, pasta_destino):
    """Baixa um arquivo PDF da URL e salva na pasta destino"""
    resposta = requests.get(url, stream=True)
    nome_arquivo = os.path.join(pasta_destino, url.split('/')[-1])
    
    with open(nome_arquivo, 'wb') as arquivo:
        for chunk in resposta.iter_content(chunk_size=128):
            arquivo.write(chunk)
    
    return nome_arquivo

def main():
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    
    # Criar estrutura de pastas
    os.makedirs('../data/raw', exist_ok=True)
    
    # Acessar site e encontrar links
    resposta = requests.get(url)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    
    # Baixar Anexos I e II
    anexos_baixados = []
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if 'Anexo I' in href or 'Anexo II' in href:
            if href.lower().endswith('.pdf'):
                print(f"Baixando: {href}")
                caminho = baixar_pdf(href, '../data/raw')
                anexos_baixados.append(caminho)
    
    # Compactar os anexos
    if anexos_baixados:
        with zipfile.ZipFile('../data/raw/anexos.zip', 'w') as zipf:
            for arquivo in anexos_baixados:
                zipf.write(arquivo, os.path.basename(arquivo))
        print("Download e compactação concluídos!")
    else:
        print("Nenhum anexo foi encontrado para download.")

if __name__ == "__main__":
    main()