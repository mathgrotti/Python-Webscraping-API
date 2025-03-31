import requests
from bs4 import BeautifulSoup
import os
import zipfile
from urllib.parse import urljoin

def baixar_pdf(url, pasta_destino, headers):
    """Baixa um arquivo PDF com tratamento de erros"""
    try:
        resposta = requests.get(url, headers=headers, stream=True, timeout=10)
        resposta.raise_for_status()  # Verifica se houve erro HTTP
        
        nome_arquivo = os.path.join(pasta_destino, url.split('/')[-1])
        
        with open(nome_arquivo, 'wb') as arquivo:
            for chunk in resposta.iter_content(chunk_size=8192):
                arquivo.write(chunk)
        
        return nome_arquivo
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
        return None

def main():
    # Configurações
    url_base = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    # Criar estrutura de pastas
    os.makedirs('../data/raw', exist_ok=True)
    
    try:
        # Acessar site
        resposta = requests.get(url_base, headers=headers, timeout=10)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Encontrar todos os links PDF
        anexos_baixados = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Verificar se é um dos anexos procurados
            if ('Anexo_I_Rol_2021RN_465.2021_RN627L.2024' in href or 'Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025' in href) and href.lower().endswith('.pdf'):
                # Construir URL completa
                url_pdf = href if href.startswith('http') else urljoin(url_base, href)
                
                print(f"Encontrado PDF: {url_pdf}")
                caminho = baixar_pdf(url_pdf, '../data/raw', headers)
                
                if caminho:
                    anexos_baixados.append(caminho)
                    print(f"Arquivo salvo em: {caminho}")
        
        # Compactar os anexos
        if anexos_baixados:
            with zipfile.ZipFile('../data/raw/anexos.zip', 'w') as zipf:
                for arquivo in anexos_baixados:
                    zipf.write(arquivo, os.path.basename(arquivo))
            print(f"\n✅ Download concluído! {len(anexos_baixados)} arquivos compactados.")
        else:
            print("\n❌ Nenhum anexo PDF foi encontrado.")
            
            # Debug: Mostrar todos os links encontrados
            print("\nLinks encontrados na página:")
            for i, link in enumerate(soup.find_all('a', href=True), 1):
                print(f"{i}. {link['href']}")
    
    except Exception as e:
        print(f"\n⚠️ Erro ao acessar a página: {e}")

if __name__ == "__main__":
    main()