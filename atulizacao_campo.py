import requests
import json
from requests.auth import HTTPBasicAuth
from comentario import add_comentario


def atualizacao_campo(ticket, url,email,api_token,linha,tabela):
    
    url = f"{url}/rest/api/2/issue/{ticket}"
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth(email, api_token)
    status = tabela.loc[linha,'Status'].upper()
    if status == "DISPONIVEL":
        camp_df = "N/A"
        camp_id = "25128"           
    else:  
         camp_df = "Defeito de utilização",
         camp_id = "25127"
    data = {
        "fields": {
          #Campo defeito do equipamento
          "customfield_15907": { 
          "value": camp_df,
          "id": camp_id
        },
        #Numero da Service Tag
        "customfield_15185": f"{tabela.loc[linha,'Service_Tag']}",
        #Campo Patrimonio 
        "customfield_14879": f"{tabela.loc[linha,'Patrimonio']}"
        }
      }

    # Envio da requisição
    response = requests.put(url, auth=auth, json=data, headers=headers)
    
    if response.status_code == 204:
        return print("Chamado atualizado com sucesso!"), add_comentario(ticket,email,api_token,url[:-14],linha=linha,tabela=tabela)#[:-15]
        
    else:
        print("Erro ao atualizar o chamado:", response.json)
