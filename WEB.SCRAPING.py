# Importando Bibliotecas
import streamlit as st
import pandas as pd
import time
import os
import shutil
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
import tkinter as tk
from selenium.webdriver import ActionChains
import matplotlib.pyplot as plt
from tkinter import messagebox
from packaging.version import Version as LooseVersion
from selenium import webdriver
from selenium_stealth import stealth




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
st.sidebar.image(r"C:\Users\cmbar\OneDrive - Tech-Data Solution\Imagens\Imagem de Apoio\infulltech.jpg", use_container_width=True)
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
def iniciar_navegador():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
    navegador = uc.Chrome(options=options)
    return navegador

# Função para simular rolagem da página para baixo
def rolar_pagina(navegador):
    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 3))  # Aguardar um pouco após a rolagem

# Função para simular digitação lenta
def digitar_lentamente(element, texto):
    for char in texto:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.5))


# Função para capturar o código do usuário manualmente com tkinter
def solicitar_codigo():
    def obter_codigo():
        global codigo
        codigo = codigo_input.get()  # Armazena o código digitado
        janela.destroy()  # Fecha a janela após clicar em "OK"

    # Cria a janela
    janela = tk.Tk()
    janela.title("Insira o Código de Verificação")
    janela.geometry("400x200")  # Ajuste o tamanho da janela (largura x altura)
    janela.configure(bg="#f0f0f0")  # Cor de fundo da janela

    # Carregar e exibir um logo, se houver
    try:
        logo = tk.PhotoImage(file="caminho/para/seu_logo.png")  # Caminho para o arquivo de imagem
        logo_label = tk.Label(janela, image=logo, bg="#f0f0f0")
        logo_label.pack(pady=5)
    except Exception as e:
        print("Erro ao carregar a imagem do logo:", e)

    # Label e campo de entrada personalizados
    tk.Label(
        janela, 
        text="Digite o código de 6 dígitos enviado para seu email:", 
        font=("Helvetica", 12),  # Fonte e tamanho da fonte
        fg="#333333",  # Cor da fonte
        bg="#f0f0f0"  # Cor de fundo do label
    ).pack(pady=10)

    # Entrada para o código
    codigo_input = tk.Entry(janela, font=("Helvetica", 14), justify="center")  # Centraliza o texto
    codigo_input.pack(pady=5)

    # Botão para enviar o código com cor personalizada
    tk.Button(
        janela, 
        text="OK", 
        command=obter_codigo, 
        font=("Helvetica", 12), 
        fg="#ffffff",  # Cor da fonte do botão
        bg="#4CAF50",  # Cor de fundo do botão
        activebackground="#45a049",  # Cor de fundo quando o botão é clicado
        activeforeground="#ffffff"  # Cor da fonte quando o botão é clicado
    ).pack(pady=10)

    # Inicia o loop da interface gráfica
    janela.mainloop()


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
#INICIO

def mensagem_fim_script():
    """
    Abre uma janela com a mensagem final indicando que o script terminou.
    """
    # Cria a janela principal
    root = tk.Tk()
    root.title("Script Finalizado")
    root.geometry("400x200")  # Define o tamanho da janela

    # Mensagem principal
    label_mensagem = tk.Label(
        root,
        text="O SCRIPT ACABOU,\nPode fechar a tela e trabalhar os dados baixados.",
        font=("Arial", 12),
        wraplength=350,  # Limita o tamanho do texto
        justify="center"
    )
    label_mensagem.pack(expand=True, pady=20)

    # Botão para fechar a janela
    btn_fechar = tk.Button(
        root,
        text="Fechar",
        font=("Arial", 10, "bold"),
        command=root.destroy,  # Fecha a janela
        bg="red",
        fg="white"
    )
    btn_fechar.pack(pady=10)

    # Mantém a janela aberta
    root.mainloop()

#FIM
# ---------------------------------------------------------------------------------------------------------------------- #




# ---------------------------------------------------------------------------------------------------------------------- #
#INICIO DO FLUXO


if processar:
    if not lista_empresas:
        st.error("Erro: Lista de empresas está vazia. Carregue o arquivo Excel antes de iniciar.")
    else:
        navegador = start_scraping()

        # Fluxo de login no portal
        colocar_email(navegador)
        colocar_senha(navegador)
        receber_cod(navegador)
        inserir_cod(navegador)
        tela_05(navegador)

        # Pesquisando a primeira empresa
        clicar_input_pesquisa(navegador)  # Clica no campo de pesquisa
        digitar_primeira_empresa(navegador)  # Digita e seleciona a empresa

        # Tenta clicar no botão 'Pedidos'
        clicar_aba_pedidos(navegador)

        # Abrir a janela de trocar loja
        clicar_trocar_loja(navegador)


        # Loop de Download
        loop(navegador, lista_empresas)

        # Chama a função ao final do script
        mensagem_fim_script()