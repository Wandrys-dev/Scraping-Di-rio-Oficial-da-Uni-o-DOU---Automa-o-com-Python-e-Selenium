import os
import time
import logging
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Diretório para salvar os resultados
LINK_OUTPUT_DIR = r"D:\\Scraping_Diario_Oficial_Uniao"

# Obtém a data do dia no formato correto (dd-mm-aaaa)
data_hoje = datetime.today().strftime("%d-%m-%Y")

# URLs das seções do DOU com a data do dia
SECOES = {
    "Sessao_01": f"https://www.in.gov.br/leiturajornal?data={data_hoje}&secao=do1",
    "Sessao_02": f"https://www.in.gov.br/leiturajornal?data={data_hoje}&secao=do2",
    "Sessao_03": f"https://www.in.gov.br/leiturajornal?data={data_hoje}&secao=do3",
}

# Configuração do ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Inicializa o ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_dou_links(url_secao):
    """Percorre todas as páginas do DOU e extrai os links das publicações da seção."""
    try:
        logging.info(f"Acessando a seção: {url_secao}")
        driver.get(url_secao)

        all_links = []
        pagina = 1

        while True:
            logging.info(f"Coletando links da página {pagina}...")

            # Espera a página carregar completamente
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-senna-off='true']"))
            )
            time.sleep(2)

            # Captura todas as publicações
            publicacoes = driver.find_elements(By.CSS_SELECTOR, "a[data-senna-off='true']")

            if not publicacoes:
                logging.warning("Nenhuma publicação encontrada.")
                break

            for publicacao in publicacoes:
                titulo = publicacao.text.strip()
                link = publicacao.get_attribute("href")
                if titulo and link and "web/dou/-/" in link:
                    all_links.append({"Título": titulo, "URL": link})

            # Verifica se há próxima página
            try:
                proxima_pagina = driver.find_element(By.XPATH, "//span[contains(@class, 'pagination-button') and text()='Próximo »']")
                if proxima_pagina:
                    proxima_pagina.click()
                    time.sleep(5)
                    pagina += 1
                else:
                    break
            except:
                break

        return all_links
    except Exception as e:
        logging.error(f"Erro ao coletar links: {e}")
        return []

def get_dou_content(url):
    """Acessa cada publicação e extrai o conteúdo textual (sem HTML)."""
    try:
        logging.info(f"Acessando publicação: {url}")
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article#materia"))
        )
        time.sleep(2)

        # Captura o conteúdo textual
        try:
            content_element = driver.find_element(By.CSS_SELECTOR, "div.texto-dou")
            full_text = content_element.text.strip()
        except:
            full_text = "Erro ao obter conteúdo"

        return {"Conteúdo": full_text}
    except Exception as e:
        logging.error(f"Erro ao acessar conteúdo de {url}: {e}")
        return {"Conteúdo": "Erro ao obter conteúdo"}

def salvar_excel(dados, nome_arquivo):
    """Salva os resultados em um arquivo Excel específico por seção, SEM a coluna HTML."""
    if not dados:
        logging.info(f"Nenhum dado encontrado para salvar: {nome_arquivo}")
        return

    if not os.path.exists(LINK_OUTPUT_DIR):
        os.makedirs(LINK_OUTPUT_DIR)

    filepath = os.path.join(LINK_OUTPUT_DIR, nome_arquivo)
    df = pd.DataFrame(dados)

    # Salvando sem coluna HTML
    df.to_excel(filepath, index=False)

    logging.info(f"✅ Arquivo salvo: {filepath}")

if __name__ == "__main__":
    for nome_secao, url_secao in SECOES.items():
        logging.info(f"\n🔹 Iniciando extração para {nome_secao}...")

        # Coleta todos os links da seção
        links_coletados = get_dou_links(url_secao)

        if links_coletados:
            logging.info(f"📌 Total de links coletados para {nome_secao}: {len(links_coletados)}")

            # Exibir os links coletados
            print(f"\n🔹 **Links coletados para {nome_secao}:**")
            print(pd.DataFrame(links_coletados))

            dados_finais = []
            for i, item in enumerate(links_coletados, 1):
                logging.info(f"🔎 Processando {i}/{len(links_coletados)}: {item['Título']}")

                # Obtém conteúdo SEM HTML
                conteudo = get_dou_content(item["URL"])
                item.update(conteudo)

                # Adiciona ao conjunto final
                dados_finais.append(item)

            # Exibir DataFrame final antes de salvar
            df_final = pd.DataFrame(dados_finais)
            print(f"\n🔹 **DataFrame final para {nome_secao}:**")
            print(df_final)

            # Nome do arquivo por seção e data
            nome_arquivo = f"{nome_secao}_{data_hoje}.xlsx"
            salvar_excel(dados_finais, nome_arquivo)

    driver.quit()  # Fecha o navegador após execução
