import requests
import json
import numpy as np
import pandas as pd
from requests.auth import HTTPBasicAuth
import os
from atulizacao_campo import atualizacao_campo
from time import sleep

import pyautogui

user = os.getenv("USERNAME")


with open(
    rf"C:\Users\{user}\Desktop\Bot_chamado_V2\automaçao_jira_API\Credencial.txt", "r"
) as cred:
    cred_txt = {}
    for txt in cred:
        txt = txt.strip()
        email, jira_url, api_token, glpi_tk = txt.split(": ", 3)


def create_Chamado(email, jira_url, api_token, linha, tabela):

    with open(
        rf"C:\Users\{user}\Desktop\Bot_chamado_V2\automaçao_jira_API\Credencial_iD.txt",
        "r",
    ) as cred_id:
        cred_i = {}
        for text in cred_id:
            text = text.strip().lower()
            nome, id = text.split(": ", 1)
            cred_i[nome] = id

        verifica_id = tabela.loc[linha, 'Tecnico'].lower()
        if verifica_id in cred_i:
            valor = cred_i[verifica_id]

    data = json.dumps(
        {
            "fields": {
                "project": {"key": "SUPPORT"},
                "issuetype": {"name": "CA - Hardware"},
                "summary": f"Analise Tecnica: {tabela.loc[linha,'Service_Tag']} - {tabela.loc[linha,'Status'].upper()}",
                "description": f"Patrimonio: {tabela.loc[linha,'Patrimonio']}\n Modelo: {tabela.loc[linha,'Modelo']}\n Service Tag: {tabela.loc[linha,'Service_Tag']}\n Garantia: {tabela.loc[linha,'Garantia'].strftime('%d/%m/%y')}\n",
                "assignee": {"accountId": valor},
                "reporter": {"accountId": "61951477d5986c006a74f2ce"},  # jhow
            },
        }
    )

    url = str(f"{jira_url.strip()}/rest/api/2/issue/")
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    auth = HTTPBasicAuth(email, api_token)

    response = requests.post(url, headers=headers, data=data, auth=auth)
    global ticket
    if response.status_code == 201:
        text = response.json()
        chave = "key"
        ticket = text[chave]
        print(
            f"chamado criado com sucesso : N°{linha} - {ticket} - {tabela.loc[linha,'Patrimonio']} - {tabela.loc[linha,'Modelo']}"
        )
        return atualizacao_campo(
            ticket=ticket,
            url=jira_url,
            api_token=api_token,
            email=email,
            linha=linha,
            tabela=tabela,
        )

    else:
        return print(f"Erro {response.status_code} - {response.text}")


if __name__ == "__main__":
    tabela = pd.read_excel(
        r"C:\Users\{0}\Desktop\Bot_chamado_V2\automaçao_jira_API\base.xlsx".format(user)
    )
    criar_pasta_pt = (
        r"C:\Users\{0}\Desktop\Bot_chamado_V2\automaçao_jira_API\Imagens".format(user)
    )
    for p in tabela.index:
        nome_Pasta = str(tabela.loc[p, "Patrimonio"])
        caminho_completo = os.path.join(criar_pasta_pt, nome_Pasta)
        os.makedirs(caminho_completo, exist_ok=True)
    pyautogui.alert("Inserir as imagens antes de continuar")
    
    for linha in tabela.index:
        print("NOVO TICKET:\n")
        create_Chamado(
            email=email,
            api_token=api_token,
            jira_url=jira_url,
            linha=linha,
            tabela=tabela,
        )
