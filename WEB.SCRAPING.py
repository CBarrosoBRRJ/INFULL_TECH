# Importando Bibliotecas


import sys
import types
if "distutils.version" not in sys.modules:
    version_module = types.ModuleType("version")
    sys.modules["distutils.version"] = version_module
    from packaging.version import Version as LooseVersion
    version_module.LooseVersion = LooseVersion

try:
    from packaging.version import Version as LooseVersion
except:
    pass

# Bibliotecas Selenium
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium_stealth import stealth


# Streamlit e Manipulação de Dados
import streamlit as st
import pandas as pd
import os
import shutil
import random
import time
from datetime import datetime

# Gráficos
import matplotlib.pyplot as plt

#Request
import requests
from msal import PublicClientApplication









### --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Variável global para armazenar a lista de empresas
lista_empresas = []

# ---------------------------------------- #
# CONFIGURAÇÃO DA INTERFACE PRINCIPAL
# ---------------------------------------- #

# Título principal
st.markdown("<h1 style='text-align: left; margin-top: 50px;'>RASPAGEM DADOS</h1>", unsafe_allow_html=True)

# Espaço adicional abaixo do título
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

# ---------------------------------------- #
# BARRA LATERAL
# ---------------------------------------- #

# Adicionando imagem no topo da barra lateral
if not os.path.exists("images/infulltech.jpg"):
    st.sidebar.error("Erro: Imagem não encontrada no caminho especificado.")
else:
    st.sidebar.image("images/infulltech.jpg", use_container_width=True)
st.sidebar.markdown("<h1 style='text-align: center; width: 100%;'>Infull Tech</h1>", unsafe_allow_html=True)

# Botão para carregar o arquivo Excel
st.sidebar.markdown("<h3 style='text-align: center; width: 100%; margin-top: -15px'>Carregar Lista de Empresas</h3>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Escolha o arquivo Excel", type=["xlsx"])

# Lógica para carregar o arquivo
if uploaded_file is not None:
    try:
        # Carrega os dados do arquivo Excel para um DataFrame
        lista_empresas_df = pd.read_excel(uploaded_file)
        st.sidebar.success("Arquivo carregado com sucesso!")

        # Trata os dados e armazena na lista de empresas
        if "Empresas" in lista_empresas_df.columns:
            dados = lista_empresas_df["Empresas"].dropna()
            lista_empresas = dados.tolist()
            st.sidebar.write(f"Total de empresas carregadas: {len(lista_empresas)}")
        else:
            st.sidebar.error("Erro: Coluna 'Empresas' não encontrada no arquivo Excel.")

    except Exception as e:
        st.sidebar.error(f"Erro ao carregar o arquivo: {e}")
else:
    st.sidebar.warning("Por favor, carregue a lista de empresas.")

# ---------------------------------------- #
# ÁREA PRINCIPAL - EXIBIÇÃO DOS DADOS
# ---------------------------------------- #

# Exibe os dados carregados (caso existam)
if lista_empresas:
    st.markdown("### Empresas Carregadas")
    st.table(pd.DataFrame(lista_empresas, columns=["Empresas"]))
else:
    st.info("Nenhuma empresa carregada ainda. Carregue o arquivo na barra lateral.")

# ---------------------------------------- #
# BOTÃO DE PROCESSAMENTO
# ---------------------------------------- #

# Botão para iniciar o processamento com chave única
processar = st.button("Iniciar Processamento", key="processar_button")
if processar:
    if not lista_empresas:
        st.error("Erro: Nenhuma lista de empresas foi carregada. Carregue o arquivo Excel.")
    else:
        st.success("Processamento iniciado...")
        # Chamadas das funções de scraping podem ser adicionadas aqui
        st.write("Executando o processo de raspagem...")


### --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Função para iniciar o navegador
import undetected_chromedriver as uc

def iniciar_navegador():
    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless")  # Executar o navegador sem interface gráfica (opcional)
        options.add_argument("--disable-blink-features=AutomationControlled")
        navegador = uc.Chrome(options=options)  # Tentativa de inicializar o navegador
        return navegador
    except Exception as e:
        print(f"Erro ao iniciar o navegador: {e}")
        return None  # Retorna None caso o navegador falhe


# Função para simular rolagem da página para baixo
def rolar_pagina(navegador):
    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 3))  # Aguardar um pouco após a rolagem

# Função para simular digitação lenta
def digitar_lentamente(element, texto):
    for char in texto:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.5))


# Substituição das funções antigas com Tkinter
def solicitar_codigo():
    st.markdown("### Insira o Código de Verificação")
    codigo = st.text_input("Digite o código de 6 dígitos enviado para seu email:", max_chars=6)
    if st.button("Enviar Código"):
        if codigo:
            st.success(f"Código inserido com sucesso: {codigo}")
            return codigo
        else:
            st.error("Por favor, insira o código.")
    return None

def exibir_mensagem_alerta(mensagem):
    st.markdown("### ⚠️ Alerta")
    st.error(mensagem)
    if st.button("Fechar"):
        st.stop()  # Encerra o script do Streamlit




# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

# Função de Raspagem Completa
def start_scraping():
    st.text("Download em Andamento...")

    # Configurações de download
    local_download = os.path.join(os.path.expanduser("~"), "Downloads")
    dir_pedidos = os.path.join(local_download, "DOWNLOAD-PEDIDOS-IFOOD")  # Cria a pasta "PEDIDOS" na pasta de Downloads do usuário

    # Verifica se a pasta "PEDIDOS" existe; caso contrário, cria a pasta
    if not os.path.exists(dir_pedidos):
        os.makedirs(dir_pedidos)
        print("Pasta 'PEDIDOS' criada na pasta de Downloads do usuário.")

    # Inicia o navegador
    navegador = iniciar_navegador()
    navegador.get('https://portal.ifood.com.br/')
    return navegador

#FIM
# ---------------------------------------------------------------------------------------------------------------------- #

# O SCRIPT COMEÇA AQUI::::

# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

#TELA 01 - COLOCAR O EMAIL

# Função para a Tela 01
def colocar_email(navegador):
    # Aguarda até que o campo de email esteja presente na página (espera até 10 segundos)
    try:
        campo_email = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]'))
        )
        digitar_lentamente(campo_email, 'portalinfull@gmail.com')

        # Define e clica no botão de login após a digitação do email
        botao_login = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/main/form/button'))
        )
        botao_login.click()
        print("Botão de login clicado.")
    except TimeoutException:
        print("O campo de email ou o botão de login não foi carregado a tempo.")

#FIM
# ---------------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

#TELA 02 - COLOCAR A SENHA

def colocar_senha(navegador):
    # Continua com o preenchimento do campo de senha
    try:
        campo_senha = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        digitar_lentamente(campo_senha, 'Portal2024@')
    except TimeoutException:
        print("O campo de senha não foi carregado a tempo.")

    # Aguarda até que o botão para submeter a senha esteja presente na página (espera até 5 segundos)
    try:
        botao_submit = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/main/form/button'))
        )
        botao_submit.click()
    except TimeoutException:
        print("O botão de submit não foi carregado a tempo.")

#FIM
# ---------------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

# TELA 03 - SELECIONAR FORMA DE RECEBER O CÓDIGO:

def receber_cod(navegador):
    # Aguarda até que o botão para submeter a senha esteja presente na página (espera até 5 segundos)
    try:
        botao_submit = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/main/div/div/div[2]/button[1]'))
        )
        botao_submit.click()
    except TimeoutException:
        print("O botão de submit não foi carregado a tempo.")

#FIM
# ---------------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

#TELA 04 - TELA DE INSERIR O CÓDIGO DE 6 DIGITOS

def inserir_cod(navegador):
    # Função para inserir o código na página após receber o email
    try:
        # Aguarda até que o campo de código esteja presente na página
        campo_codigo = WebDriverWait(navegador, 60).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/main/div/form/div[2]/div[1]/input'))
        )

        # Solicita o código manualmente
        solicitar_codigo()

        # Insere o código no campo após o usuário digitar e pressionar "OK"
        if codigo:
            campo_codigo.send_keys(codigo)
            print("Código inserido com sucesso.")
        else:
            print("Nenhum código foi inserido.")

    except TimeoutException:
        print("O campo de código não foi carregado a tempo.")

#FIM
# ---------------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

# TELA 05 - APENTANDO EM AVANÇAR DEPOIS DE DIGITAR O CODIGO DE 6 DIGITOS

def tela_05(navegador):
    # Aguarda até que o botão para submeter a senha esteja presente na página (espera até 5 segundos)
    try:
        botao_submit = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/main/div/form/div[4]/button[1]'))
        )
        botao_submit.click()
    except TimeoutException:
        print("O botão de submit não foi carregado a tempo.")

#FIM
# ---------------------------------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

## CLICAR NA DIGITAÇÃO
local_digitacao = '//*[@id="pomodoro-modal-root"]/div/div[1]/div[2]/div[1]/div[1]/div/input'

def clicar_input_pesquisa(navegador):
    try:
        botao_submit = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.XPATH, local_digitacao))
        )
        print("O botão de submit foi carregado a tempo.")
        botao_submit.click()

    except TimeoutException:
        print("O botão de submit não foi carregado a tempo.")


#FIM
# ---------------------------------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

# XPath do campo de entrada para pesquisa
campo_pesquisa_xpath = '//*[@id="pomodoro-modal-root"]/div/div[1]/div[2]/div[1]/div[1]/div/input'

# XPath do primeiro item da lista de sugestões
primeira_sugestao_xpath = '//*[@id="pomodoro-modal-root"]/div/div[1]/div[2]/div[2]/ul/li/div[2]'

def digitar_primeira_empresa(navegador):
    try:
        # Localizando o campo de entrada (pesquisa)
        campo_pesquisa = WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.XPATH, campo_pesquisa_xpath))
        )
        
        # Digitando a primeira empresa da lista
        digitar_lentamente(campo_pesquisa, lista_empresas[0])
        print(f"Empresa '{lista_empresas[0]}' digitada com sucesso.")
        time.sleep(3)  # Tempo para carregar as sugestões

        # Selecionando o primeiro item da lista de sugestões
        primeira_sugestao = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, primeira_sugestao_xpath))
        )
        primeira_sugestao.click()
        print("Primeira sugestão selecionada com sucesso.")

    except TimeoutException:
        print("O campo de pesquisa ou a sugestão não foi localizada, favor rever o script com o administrador.")


#FIM
# ---------------------------------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO


# TELA 07 - CLICAR EM PEDIDOS
# Novo nome para o XPath da aba de pedidos

xpath_aba_pedidos = '//*[@id="app"]/div[1]/div[1]/div/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[3]/a/div/div[1]/div'

def clicar_aba_pedidos(navegador):
    try:
        
        # XPath do botão 'Pedidos'
        xpath_botao_pedidos = '//*[@data-testid="sidebar-item-orders"]'

        # Localiza o botão 'Pedidos'
        botao_pedidos = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath_botao_pedidos))
        )

        # Força o clique com JavaScript para evitar interceptações
        navegador.execute_script("arguments[0].click();", botao_pedidos)
        print("Botão 'Pedidos' clicado com sucesso.")
        # Aguarda o carregamento completo da página
        WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
    except Exception as e:
        print(f"Erro ao clicar no botão 'Pedidos': {e}")




#FIM
# ---------------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

# ATUALIZAR PAGINA APERTANDO F5

def funcao_atualizar_pag(navegador):
    try:
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        navegador.refresh()
        print("Página atualizada com sucesso.")
        # Aguarda o carregamento completo da página
        WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")

    except Exception as e:
        print(f"Erro ao atualizar a página: {e}")


#FIM
# ---------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

def clicar_trocar_loja(navegador):
    xpath_trocar_loja = '//*[@id="app"]/div[1]/div[1]/div/div[3]/div[1]/div/div/div/div/div/div[1]/div[2]/div/div[1]/button'
    try:
        # Clicar na aba "Trocar Loja"
        print("Tentando clicar no botão de TROCAR LOJA...")
        bnt_trocar_loja = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath_trocar_loja))
        )
        # Aguarda o carregamento completo da página
        WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        bnt_trocar_loja.click()
        print("BOTAO TROCAR LOJA clicado com sucesso.")
        time.sleep(2)  # Tempo para carregar as sugestões


    except TimeoutException:
        print("O robô demorou muito a partar o botão.")



# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO

# Função para simular digitação lenta
def digitar_lentamente_2(element, texto):
    for char in texto:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.2))


#FIM
# ---------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO


def loop(navegador, lista_empresas):
    """
    Processa a lista de empresas para digitar, selecionar e acessar a aba pedidos.
    """
    # XPath para os elementos necessários no loop
    xpath_campo_pesquisa = '//*[@id="pomodoro-modal-root"]/div/div[1]/div[2]/div[1]/div[1]/div/input'
    xpath_selecionando_empresa = '//*[@id="pomodoro-modal-root"]/div/div[1]/div[2]/div[2]/ul/li/div[2]'

    xpath_btn_todos_filtros = '//*[@id="micro-frontend-orders"]/div[2]/div[3]/div/form/div/div[4]/button'
    xpath_btn_periodos = '//*[@id="pomodoro-modal-root"]/div/div[1]/div[3]/div/div[3]/div[1]'
    xpath_btn_30dias = '//*[@id="pomodoro-modal-root"]/div/div[1]/div[3]/div/div[3]/div[2]/div/div[1]/button[3]'
    xpath_btn_filtrar = '//*[@id="pomodoro-modal-root"]/div/div[1]/div[4]/div/button[2]'

    xpath_exportar = '//*[@id="micro-frontend-orders"]/div[2]/div[3]/div/div[2]/div/button'

    xpath_esta_loja = '//*[@id="micro-frontend-orders"]/div[2]/div[3]/div/div[2]/div/div/button[1]'


    for i, empresa in enumerate(lista_empresas):
        print(f"\nProcessando empresa {i + 1}/{len(lista_empresas)}: {empresa}")
        
        try:
            # Localiza o campo de entrada para pesquisa
            campo_pesquisa = WebDriverWait(navegador, 15).until(
                EC.visibility_of_element_located((By.XPATH, xpath_campo_pesquisa))
            )
            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")

            campo_pesquisa.click()
            print("Campo de pesquisa clicado com sucesso.")

            # Digita o nome da empresa atual
            campo_pesquisa.clear()
            digitar_lentamente_2(campo_pesquisa, empresa)
            print(f"Empresa '{empresa}' digitada com sucesso.")
            time.sleep(2)  # Tempo para carregar as sugestões

            # Seleciona a primeira sugestão
            primeira_sugestao = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_selecionando_empresa))
            )
            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")

            primeira_sugestao.click()
            print(f"Empresa '{empresa}' selecionada com sucesso.")



            ## ETAPAS DE FILTROS
            

            # Clicar no Botão de Filtros
            todos_filtros = WebDriverWait(navegador, 15).until(
                EC.visibility_of_element_located((By.XPATH, xpath_btn_todos_filtros))
            )
            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            todos_filtros.click()
            print("TODOS OS FILTROS clicado com sucesso.")



            # Clicar no Botão de PERIODOS
            btn_periodos = WebDriverWait(navegador, 15).until(
                EC.visibility_of_element_located((By.XPATH, xpath_btn_periodos))
            )
            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            btn_periodos.click()
            print("PERIODO clicado com sucesso.")



            # Clicar no Botão de 30 DIAS
            btn_30_dias = WebDriverWait(navegador, 15).until(
                EC.visibility_of_element_located((By.XPATH, xpath_btn_30dias))
            )
            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            btn_30_dias.click()
            print("30 DIAS clicado com sucesso.")


            
            # Clicar no Botão de APLICAR FILTROS
            aplicar_filtros = WebDriverWait(navegador, 15).until(
                EC.visibility_of_element_located((By.XPATH, xpath_btn_filtrar))
            )
            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            aplicar_filtros.click()
            print("FILTROS APLICADOS clicado com sucesso.")

            
            ## ETAPAS DE EXPORTAR

            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")


            try:
                xpath_exportar = '//*[@id="micro-frontend-orders"]/div[2]/div[3]/div/div[2]/div/button'
                    
                # Aguarda o botão ficar visível e clicável
                btn_exportar = WebDriverWait(navegador, 15).until(EC.element_to_be_clickable((By.XPATH, xpath_exportar)))
                    
                # Garante que a página esteja completamente carregada
                WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                    
                # Tenta clicar no botão
                btn_exportar.click()
                print("BOTAO EXPORTAR clicado com sucesso.")
            except Exception as e:

                # Aguarda o carregamento completo da página
                WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                    
                # Localiza o elemento e clica
                xpath = '//*[@id="micro-frontend-orders"]/div[2]/div[3]/div/div[1]/div/button'
                botao_exportar = navegador.find_element(By.XPATH, xpath)
                botao_exportar.click()
                print("BOTÃO EXPORTAR clicado com sucesso.")

            # Clicar no Botão de ESTA LOJA
            time.sleep(1)  # Tempo para carregar as sugestões


            tentativas = 5  # Número máximo de tentativas

            for tentativa in range(1, tentativas + 1):
                try:
                    print(f"\nTentativa {tentativa} de clicar no BOTÃO ESTA LOJA...")

                    # Aguarda o botão ser visível e clicável
                    btn_esta_loja = WebDriverWait(navegador, 15).until(
                        EC.visibility_of_element_located((By.XPATH, xpath_esta_loja))
                    )
                    
                    # Aguarda o carregamento completo da página
                    WebDriverWait(navegador, 30).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )

                    # Tenta clicar no botão
                    btn_esta_loja.click()
                    print("BOTÃO ESTA LOJA clicado com sucesso.")
                    break  # Sai do loop se clicar com sucesso


                except Exception as e:

                    time.sleep(2)  # Pequena pausa para garantir carregamento

                    # Tenta localizar e clicar em outro XPath alternativo
                    xpath_2 = '//*[@id="micro-frontend-orders"]/div[2]/div[3]/div/div[1]/div/div/button[1]'

                    WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")

                    btn_esta_loja_2 = navegador.find_element(By.XPATH, xpath_2)
                    btn_esta_loja_2.click()

                    print("BOTÃO ALTERNATIVO ESTA LOJA clicado com sucesso.")
                    break  # Sai do loop se clicar com sucesso no botão alternativo


                    # Aguarda carregamento da página antes de nova tentativa
                    print("Recarregando a página para tentar novamente...")
                    print(f"Erro ao clicar no BOTÃO ESTA LOJA na tentativa {tentativa}: {e}") 

                    WebDriverWait(navegador, 30).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )

            else:
                # Caso todas as tentativas falhem
                print("Falha: Não foi possível clicar no BOTÃO ESTA LOJA após 3 tentativas.")
                raise Exception("Falha ao clicar no BOTÃO ESTA LOJA.") 



                
            ## ETAPA DE CRIAR PASTA, RENOMEAR E MOVER ARQUIVO



            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(3)  # Tempo adicional para garantir o download completo

            # Diretório de download padrão
            local_download = os.path.join(os.path.expanduser("~"), "Downloads")
            # Diretório "DOWNLOAD-PEDIDOS-IFOOD" onde os arquivos serão salvos
            dir_pedidos = os.path.join(local_download, "DOWNLOAD-PEDIDOS-IFOOD")

            # Verifica se a pasta "DOWNLOAD-PEDIDOS-IFOOD" existe; caso contrário, cria a pasta
            if not os.path.exists(dir_pedidos):
                os.makedirs(dir_pedidos)
                print(f"Pasta '{dir_pedidos}' criada com sucesso.")
            else:
                print(f"Pasta '{dir_pedidos}' já existe.")

            # Renomeia e move o arquivo baixado SE ele contiver "lista-de-pedidos" no nome
            data_atual = datetime.now().strftime("%Y-%m-%d")
            novo_nome_arquivo = f"{empresa}_{data_atual}.xlsx"  # Nome do novo arquivo

            # Lista os arquivos ".xlsx" na pasta Downloads e filtra os que contêm "lista-de-pedidos"
            arquivos_download = [
                f for f in os.listdir(local_download)
                if f.endswith(".xlsx") and "lista-de-pedidos" in f.lower()
            ]

            if arquivos_download:
                # Pega o arquivo correto (o mais recente contendo "lista-de-pedidos")
                arquivo_baixado = max(
                    arquivos_download,
                    key=lambda f: os.path.getctime(os.path.join(local_download, f))
                )

                caminho_antigo = os.path.join(local_download, arquivo_baixado)
                caminho_novo = os.path.join(dir_pedidos, novo_nome_arquivo)  # Caminho de destino

                # Se o arquivo já existir na pasta de destino, substitui
                if os.path.exists(caminho_novo):
                    os.remove(caminho_novo)  # Remove o arquivo existente
                    print(f"Arquivo existente '{novo_nome_arquivo}' foi removido para substituição.")

                # Move o arquivo renomeado para a pasta de destino
                shutil.move(caminho_antigo, caminho_novo)
                print(f"Arquivo '{arquivo_baixado}' renomeado para '{novo_nome_arquivo}' e movido para: {dir_pedidos}")
            else:
                print("Nenhum arquivo com o nome 'lista-de-pedidos' foi encontrado na pasta Downloads.")
                # Se necessário, apenas continua o script




            # ATUALIZAR A PAGINA
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            navegador.refresh()
            print("Página atualizada com sucesso.")
            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")



            ## ETAPA DE ABRIR A JANELA PARA TROCAR A EMPRESA

            # Clicar no "clicar_trocar_loja" após selecionar a empresa

            # Aguarda o carregamento completo da página
            WebDriverWait(navegador, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")

            clicar_trocar_loja(navegador)
            print("Aba de pedidos acessada com sucesso.")

            time.sleep(2)  # Pequena pausa antes de processar a próxima empresa

        except TimeoutException as e:
            print(f"Erro ao processar a empresa '{empresa}': {e}")
            continue  # Continua para a próxima empresa em caso de erro

#FIM
# ---------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------------------------------------------------- #
# INICIO DO FLUXO

if processar:
    if not lista_empresas:
        st.error("Erro: Lista de empresas está vazia. Carregue o arquivo Excel antes de iniciar.")
    else:
        st.success("Iniciando o processo de raspagem...")
        
        # Inicializa o navegador
        navegador = start_scraping()
        
        # Fluxo de login no portal
        st.write("Realizando login no portal...")
        colocar_email(navegador)
        colocar_senha(navegador)
        
        # Recebe o código de verificação
        st.markdown("### Recebendo Código de Verificação")
        receber_cod(navegador)  # Simula o recebimento do código no navegador
        
        # Solicita o código manualmente via Streamlit
        codigo = solicitar_codigo()
        if not codigo:
            exibir_mensagem_alerta("Erro: Código de verificação não foi fornecido. Processo encerrado.")
            st.stop()
        
        # Insere o código no navegador
        inserir_cod(navegador, codigo)  # Ajuste a função para aceitar o código como argumento
        
        # Continuação do fluxo
        st.write("Processo de login concluído, prosseguindo com a raspagem...")
        tela_05(navegador)

        # Pesquisando a primeira empresa
        st.write("Pesquisando a primeira empresa...")
        clicar_input_pesquisa(navegador)  # Clica no campo de pesquisa
        digitar_primeira_empresa(navegador)  # Digita e seleciona a empresa

        # Tenta clicar no botão 'Pedidos'
        st.write("Clicando na aba 'Pedidos'...")
        clicar_aba_pedidos(navegador)

        # Abrir a janela de trocar loja
        st.write("Abrindo janela de troca de loja...")
        clicar_trocar_loja(navegador)

        # Loop de Download
        st.write("Iniciando o loop de download...")
        loop(navegador, lista_empresas)

        # Mensagem final do script
        mensagem_fim_script()
        st.success("Processo de raspagem concluído com sucesso!")
