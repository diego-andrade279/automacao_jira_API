import requests
import json
from requests.auth import HTTPBasicAuth
from Glpi_integraçao import integracao_Glpi

def trandition_Statu(email, api_token, ticket, url,tabela,linha):
    # Substitua pelos seus valores
    url = f"{url}/{ticket}/transitions"

    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = HTTPBasicAuth(email, api_token)
    modelo = tabela.loc[linha,'Modelo'].lower().split()
    if modelo[0] == "macbook":
        valor = modelo[0].capitalize()
    else:
        valor = "Notebook"
    data = {
        # Transiçao de Aberto para Em andamento
        "transition": {"id": "21", "name": "Classificação"},
        # campo Serviço e classificaçao
        "fields": {
            "customfield_14051": {"id": "15949", "value": valor},
            # campo frente de atendimento
            "customfield_19857": {"id": "34854", "value": "iFood"},
        }
    }
    #validaçao campo troca
    validacao = tabela.loc[linha, 'Estado_Equipamento']
    if validacao == "USADO":
        valor = "Sim"
        id_x = "30628"
    else:
        valor = "Não"
        id_x = "30629"

    data_resolvido ={
        #transiçao para resolvido 
        "transition": {"id": "51", "name": "Resolvido"},
        #campo troca 
        "fields": {
            "customfield_18105": {"value": valor,"id": id_x}
         }
        }
    # Envio da requisição usando metodo POST
    response = requests.post(url, auth=auth, json=data, headers=headers)
    response_resolvido = requests.post(url, auth=auth, json=data_resolvido, headers=headers)
    if response.status_code == 204:
        print(f"Chamado atualizado com sucesso : {response.status_code}(Chamado Em andamento) Para {response_resolvido.status_code} (Chamado resolvido) ")
        return integracao_Glpi(ticket=ticket,tabela=tabela,linha=linha)
    else:
        print("Erro ao atualizar o chamado:", response.json,response_resolvido.json)
