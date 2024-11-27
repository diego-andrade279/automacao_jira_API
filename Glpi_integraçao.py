from datetime import datetime
import pandas as pd
import ctypes
import os
import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)
from time import sleep
import time

ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
user_name = os.getenv("USERNAME")

# ##########################################################################


def integracao_Glpi(ticket, tabela, linha):
    numero_Ticket = ticket
    ini = time.time()

    options = Options()
    s = Service(ChromeDriverManager().install())
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    options.add_argument("--force-device-scale-factor=0.79")
    options.add_argument("--profile-directory=Default")
    options.add_argument(
        r"--user-data-dir=C:\Users\{0}\AppData\Local\Google\Chrome\User Data".format(
            user_name
        )
    )

    st = tabela.loc[linha, "Service_Tag"]
    pt = tabela.loc[linha, "Patrimonio"]
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(
        f"https://inventory.ifoodcorp.com.br/front/computer.php?is_deleted=0&as_map=0&browse=0&criteria%5B0%5D%5Blink%5D=AND&criteria%5B0%5D%5Bfield%5D=view&criteria%5B0%5D%5Bsearchtype%5D=contains&criteria%5B0%5D%5Bvalue%5D={st}&itemtype=Computer&start=0&_glpi_csrf_token=51691ee852929c2669adf0a485cb1a60204963f4b6c129dccca56918a9735867&sort%5B%5D=1&order%5B%5D=ASC"
    )
    sleep(10)

    id_comput = 'a[id^="Computer_"]'
    camp_Patrimonio = driver.find_element(By.CSS_SELECTOR, id_comput)
    id_comput = camp_Patrimonio.get_attribute("id")
    camp_Patrimonio = driver.find_element(By.ID, id_comput)
    camp_Patrimonio.click()
    sleep(5)
    driver.find_element(
        By.CSS_SELECTOR, 'a.nav-link[title="Informações Gerais"]'
    ).click()
    sleep(2.5)

    tc = tabela.loc[linha, "Tecnico"].split()
    print(f"Analista Responsavel: {tc[0]}")
    camp_Analista = driver.find_element(
        By.CSS_SELECTOR, 'input[id^="analistaatfieldtwo_"]'
    )
    camp_Analista.clear()
    camp_Analista.send_keys(str(tc[0]), " ", str(tc[-1]))
    sleep(1.5)

    camp_Tp_Analise = driver.find_element(By.CSS_SELECTOR, '[data-select2-id="29"]')
    sleep(1.5)
    camp_Tp_Analise.click()
    sleep(1)

    # Campo Tipo de analise
    try:
        class_pai = "ul.select2-results__options"  # nome da class do menu suspenso
        camp_Tp_Analise2 = driver.find_element(By.CSS_SELECTOR, class_pai)
        id_pai = camp_Tp_Analise2.get_attribute("id")
        pai = f"#{id_pai} li[title='Análise Técnica - '] > span[title='Análise Técnica - ']"
        camp_Tp_Analise2 = driver.find_element(By.CSS_SELECTOR, pai)
        camp_Tp_Analise2.click()
        sleep(1.5)
        print("Passo de seleçao em  Analise Tecnica:")
    except NoSuchElementException:
        pass
        sleep(1.5)

    # Campo Data da Analise
    class_input_data = "div.input-group.flatpickr"
    camp_Data = driver.find_element(By.CSS_SELECTOR, class_input_data)
    id_input = camp_Data.get_attribute("id")
    camp_Data = driver.find_element(By.ID, id_input)
    camp_Data.click()
    print("Passo de seleçao Da Data dia atual concluido:")
    sleep(1.5)

    camp_Data2 = driver.find_element(
        By.CSS_SELECTOR, 'button.ms-2.btn.btn-outline-secondary[btn-id="0"]'
    )
    camp_Data2.click()
    sleep(1.5)

    # Campo Numero do chamado
    id_n_Ticket = 'input[name="ndechamadodeatfield"]'
    camp_N_chamado = driver.find_element(By.CSS_SELECTOR, id_n_Ticket)
    id_n_Ticket = camp_N_chamado.get_attribute("id")
    camp_N_chamado = driver.find_element(By.ID, id_n_Ticket)
    camp_N_chamado.click()
    sleep(1.5)
    camp_N_chamado.clear()
    sleep(1.5)
    camp_N_chamado.send_keys(str(numero_Ticket))
    sleep(1.5)
    print("Campo N° ticket concluido:")

    # Estado do equipamento
    camp_estado_EQ = driver.find_element(
        By.CSS_SELECTOR,
        '[id^="select2-dropdown_plugin_fields_estadodoequipamentoemestoquefielddropdowns_id"]',
    )
    camp_estado_EQ = camp_estado_EQ.get_attribute("id")
    camp_estado_EQ = driver.find_element(By.ID, camp_estado_EQ)
    camp_estado_EQ.click()
    sleep(1)

    status = tabela.loc[linha, "Status"].upper()
    print("Validaçao do estado do equipamento:")
    if status == "DISPONIVEL":
        x = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
        sleep(2.5)
        x.send_keys(str(status))
        sleep(1)
        x.send_keys(Keys.ENTER)
        sleep(1.5)

    elif status == "FABRICANTE":
        x = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
        sleep(2.5)
        x.send_keys(str(status))
        sleep(1)
        x.send_keys(Keys.ENTER)
        sleep(1.5)

    elif status == "DESCARTE":
        x = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
        sleep(2.5)
        x.send_keys(str(status))
        sleep(1)
        x.send_keys(Keys.ENTER)
        sleep(1.5)

    elif status == "BATERIA":
        x = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
        sleep(2.5)
        x.send_keys(str(status))
        sleep(1)
        x.send_keys(Keys.ENTER)
        sleep(1.5)

    elif status == "DEFEITO":
        x = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
        sleep(2.5)
        x.send_keys(str(status))
        sleep(1)
        x.send_keys(Keys.ENTER)
        sleep(1.5)

    elif status == "FORA DO PARQUE":
        x = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
        sleep(2.5)
        x.send_keys(str(status))
        sleep(1)
        x.send_keys(Keys.ENTER)
        sleep(1.5)

    # localizaçao estoque
    camp_loc_estoque = driver.find_element(
        By.CSS_SELECTOR,
        '[id^="select2-dropdown_plugin_fields_localizaonoestoquefielddropdowns_id"]',
    )
    camp_estado_EQ = camp_estado_EQ.get_attribute("id")
    camp_estado_EQ = driver.find_element(By.ID, camp_estado_EQ)
    camp_loc_estoque.click()
    print("Localizaçao do equipamento no estoque:")
    sleep(1.5)

    # campo prateleras
    camp_prateleira = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
    fabri = tabela.loc[linha, "Fabricante"].upper().strip()

    # Processo logico para alocar os equipamento
    processador = str(tabela.loc[linha, "Processador"]).upper().strip()
    modelo = tabela.loc[linha, "Modelo"].strip()
    print("Validando Local na prateleira")
    if status == "DISPONIVEL":

        if (
            modelo == "Latitude 3440 i7 16GB"
            and processador == "I7"
            and status == "DISPONIVEL"
        ):
            camp_prateleira.send_keys(str("D3C1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

        elif (
            modelo == "Latitude 3440 i7 16GB"
            and processador == "I5"
            and status == "DISPONIVEL"
        ):
            camp_prateleira.send_keys(str("D3B1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

        elif processador == "I7" and fabri == "DELL" or fabri == "DELL INC.":
            camp_prateleira.send_keys(str("D2B1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

        elif processador == "I7" and fabri == "LENOVO":
            camp_prateleira.send_keys(str("D1B1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

        elif processador == "I5" and fabri == "DELL" or fabri == "DELL INC.":
            camp_prateleira.send_keys(str("D5B1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

        elif processador == "I5" and fabri == "LENOVO":
            camp_prateleira.send_keys(str("D5C1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

        elif processador == "I5" and fabri == "APPLE" or fabri == "APPLE INC.":
            camp_prateleira.send_keys(str("D25B1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

        elif processador == "I7" and fabri == "APPLE" or fabri == "APPLE INC.":
            camp_prateleira.send_keys(str("D25B1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

        elif (
            (processador == "M1" and fabri == "APPLE" or fabri == "APPLE INC.")
            or (processador == "M2" and fabri == "APPLE" or fabri == "APPLE INC.")
            or (processador == "M3" and fabri == "APPLE" or fabri == "APPLE INC.")
        ):
            camp_prateleira.send_keys(str("D21B1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

    elif status == "FABRICANTE":

        if processador == "I7" and status == "FABRICANTE":
            camp_prateleira.send_keys(str("AT4B1"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

        elif processador == "I5" and status == "FABRICANTE":
            camp_prateleira.send_keys(str("AT4B2"))
            sleep(2)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2.5)

            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

    elif status == "DESCARTE":

        if fabri == "DELL":
            camp_prateleira.send_keys("D15D1")
            sleep(1.5)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2)
            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

        elif fabri == "LENOVO":
            camp_prateleira.send_keys("D11B1")
            sleep(1.5)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2)
            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

        elif fabri == "APPLE":
            camp_prateleira.send_keys("D14B1")
            sleep(1.5)
            camp_prateleira.send_keys(Keys.ENTER)
            sleep(2)
            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)
        else:
            print("Opcao nao encontrada!!!")
            pass
    # BATERIA
    elif status == "BATERIA":
        hoje = datetime.now().strftime("%d/%m/%Y")
        garantia = tabela.loc[linha, "Garantia"].strftime("%d/%m/%y")

        if fabri == "DELL":
            if hoje >= garantia:  # maquinas bateria sem garantia
                camp_prateleira.send_keys("D10C1")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            else:  # maquinas bateria com garantia
                camp_prateleira.send_keys("D10B1")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)

            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Bateria")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("BATERIA")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

        elif fabri == "LENOVO":
            if hoje >= garantia:  # maquinas bateria sem garantia
                camp_prateleira.send_keys("D10C1")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            else:  # maquinas bateria com garantia
                camp_prateleira.send_keys("D10B1")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("BATERIA")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("BATERIA")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

        elif fabri == "APPLE":
            if hoje >= garantia:  # maquinas bateria sem garantia
                camp_prateleira.send_keys("D14B4")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            else:  # maquinas bateria com garantia
                camp_prateleira.send_keys("D14B4")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("BATERIA")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)
        #################################################################################
    elif status == "Fora do Parque":
        hoje = datetime.now().strftime("%d/%m/%Y")
        garantia = tabela.loc[linha, "Garantia"].strftime("%d/%m/%y")

        if fabri == "DELL":
            if hoje >= garantia:  # maquinas bateria sem garantia
                camp_prateleira.send_keys("D14B1")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            else:  # maquinas bateria com garantia
                camp_prateleira.send_keys("D14B1")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)

            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Fora do Parque")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Fora do Parque")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

        elif fabri == "LENOVO":
            if hoje >= garantia:  # maquinas bateria sem garantia
                camp_prateleira.send_keys("D14C1")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            else:  # maquinas fora do parque com garantia
                camp_prateleira.send_keys("D14B1")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Fora do Parque")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Fora do Parque")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

        elif fabri == "APPLE":
            if hoje >= garantia:  # maquinas bateria sem garantia
                camp_prateleira.send_keys("D14B4")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            else:  # maquinas bateria com garantia
                camp_prateleira.send_keys("D14B4")
                sleep(1.5)
                camp_prateleira.send_keys(Keys.ENTER)
                sleep(2)
            try:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="35"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Fora do Parque")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)

            except NoSuchElementException:
                cam_defeito = driver.find_element(
                    By.CSS_SELECTOR, '[data-select2-id="13"]'
                )
                cam_defeito.click()
                sleep(1.5)

                cam_input_defeito = driver.find_element(
                    By.CSS_SELECTOR, "input.select2-search__field"
                )
                cam_input_defeito.send_keys("Placa Mae")
                sleep(2)
                cam_input_defeito.send_keys(Keys.ENTER)
                sleep(1.5)



        ###################################################################################
        else:
            print("Opcao nao encontrada!!!")

    else:
        pass
    print("Adicionando OBS:")
    # CAMPO 0BSERVAÇAO
    camp_obs = driver.find_element(By.CSS_SELECTOR, '[name="observaofieldthree"]')
    camp_obs.click()
    sleep(1)
    camp_obs.clear()
    sleep(1)
    camp_obs.send_keys("Analise tecnica relizada com sucesso: -" + str(numero_Ticket))
    sleep(1.5)

    # botao salve
    bot_salve = driver.find_element(By.CSS_SELECTOR, '[name="update_fields_values"]')
    bot_salve.click()
    sleep(2.5)

    driver.quit()
    fim = time.time()
    tem_exe = (fim - ini) / 60
    print(f"Tempo de execuçao: {tem_exe:.2f} minutos")
    tem_exe = 0

    return print(f"Glpi Atualizado com Sucesso: {numero_Ticket} - {status}:\n\n")
