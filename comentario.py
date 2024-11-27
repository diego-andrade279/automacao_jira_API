import requests
import json
from requests.auth import HTTPBasicAuth
from time import sleep
from Trasition_Andamento import trandition_Statu
import os

user = os.getenv("USERNAME")


def add_comentario(ticket, email, api_token, url, linha, tabela):
    """
    BLOCO DE ADICIONAR COMENTARIOS
    """
    img_url = url
    url = f"{url}{ticket}/comment"
    
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = HTTPBasicAuth(email, api_token)
    with open(
        r"C:\Users\{0}\Desktop\Bot_Ticket\main\Res_cliente.txt".format(user), "r"
    ) as cliente:
        chave_txt = {}
        for txt in cliente:
            txt = txt.strip()
            chave, valor = txt.split(": ", 1)
            chave_txt[chave] = valor

        verificacao = tabela.loc[linha, "Status"].upper()
        if verificacao in chave_txt:
            novo_valor = chave_txt[verificacao]

    respond_cli = {"body": f"{verificacao}: {novo_valor}"}
    # Envio da requisição Adicionar comentario
    response = requests.post(url, auth=auth, json=respond_cli, headers=headers)
    ###################################################################################
    """
    BLOCO DE ANEXO DE IMAGENS 
    """
    # Adicionar imagens a requisiçao
    url_imagens = f"{img_url}{ticket}/attachments"
    auth_img = HTTPBasicAuth(email, api_token)
    headers_img = headers = {
        "X-Atlassian-Token": "no-check",
        "Accept": "application/json",
        
    }
    files = []
    # Adicionar imagens ao formulario
    diretorio_imagens = rf"C:\Users\{user}\Desktop\Bot_chamado_V2\automaçao_jira_API\Imagens\{str(tabela.loc[linha,'Patrimonio'])}"
    # Listar todas as imagens na pasta
    imagens = os.listdir(diretorio_imagens)
    for imagem in imagens:
        if imagem.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            caminho = os.path.join(diretorio_imagens, imagem)
            files.append(('file',(imagem, open(caminho, 'rb'))))

            # Envio de requisiçao Adicionar anexos
    response2 = requests.post(url_imagens, auth=auth_img, files=files, headers=headers_img)
    
    if response.status_code == 201 and response2.status_code == 200:
        print(
            f"Comentário adicionado com sucesso! Status: {response.status_code}"
        )
        return print(f"Imagem adicionada com sucesso! Status :{response2.status_code}"), trandition_Statu(
            email=email, api_token=api_token, ticket=ticket, url=url[:-23],tabela=tabela,linha=linha
        )

    else:
        print("Erro ao atualizar o chamado:", response2.json, response2.text)
