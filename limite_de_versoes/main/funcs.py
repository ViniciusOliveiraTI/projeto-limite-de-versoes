import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega o caminho do arquivo
load_dotenv(f'{Path(r'settings.env').absolute()}')

# Obtém as variáveis
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Criando Objeto para obter o token de acesso
class AccessToken:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        # Todas as variáveis necessárias
        self.tenant_id, self.client_id, self.client_secret = tenant_id, client_id, client_secret
    
    # Método para obter token de acesso
    def get_access_token(self):
        try:
            url = f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token' # URL responsável pela API de autenticação

            # Parâmentros requisitados pela API do graph
            param = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'https://graph.microsoft.com/.default'
            }

            # Solicitando API
            response = requests.post(url, data=param)
            response.raise_for_status() # Cria um erro caso exista um

            # Validando token
            if response.status_code == 200:
                
                # Cria o token de acesso e o cabeçalho
                access_token = response.json().get('access_token')
                headers = {'Authorization': f'Bearer {access_token}'}

                return {'status': True, 'access_token': access_token, 'headers': headers}  # Retorna o token de acesso
            
            # Retorna nada
            return {'status': False, 'access_token': None, 'headers': None, 'error': f'Falha ao obter token de acesso: {response.json()}'}
        
        except requests.exceptions.HTTPError as http_err:
                return {'status': False, 'error': f'Erro HTTP ao obter sites: {str(http_err)}'}
        
        except requests.exceptions.RequestException as req_err:
                return {'status': False, 'error': f'Erro ao obter conexão: {str(req_err)}'}
            
        except Exception as err:
            return {'status': False, 'error': f'Erro inesperado: {str(err)}'}

# Objeto SharePoint para operações relacionadas
class SharePoint:
    def __init__(self):

        # Variáveis necessárias
        self.access_token = None  
        self.headers = None

    def auth(self):
        try:
            # Cria um objeto para o token de autenticação
            tokenObj = AccessToken(
                TENANT_ID, 
                CLIENT_ID, 
                CLIENT_SECRET
                )

            # Obtem o token de acesso e o header
            result = tokenObj.get_access_token()
            if result.get('status'): # Verfificação

                # Alimenta novamente o header e o token
                self.access_token = result.get('access_token')
                self.headers = result.get('headers')

                # Retorna status positivo
                return {'status': True}
            
            # Retorna erro
            return {'status': False, 'error': result.get('error')}
        
        # Execeção em casos de erro ao validar token
        except Exception as err:
            return {'status': False, 'error': f'Erro inesperado {str(err)}'}
    
    # Método para listar todos os sites do SharePoint
    def get_all_sites(self):
        
        # Cria a autenticação
        result = self.auth()
        if result.get('status'): # Valida o status

            try:
                url = 'https://graph.microsoft.com/v1.0/sites?search=*' # URL que encontra todos os sites
                
                # Solicitação de conexão com a API
                response = requests.get(url, headers=self.headers)
                response.raise_for_status() # Levanta um erro caso ocorra problemas de execução

                # Verificação se foi possível se conectar
                if response.status_code == 200:

                    # Obtem todos os sites
                    sites = response.json().get('value')

                    # Retorna os dados
                    return {'status': True, 'data': sites}
            
                # Problema ao executar o request
                return {'status': False, 'error': response.json()}
            
            # Tratamento de exceções
            except requests.exceptions.HTTPError as http_err:
                return {'status': False, 'error': f'Erro HTTP ao obter sites: {str(http_err)}'}
        
            except requests.exceptions.RequestException as req_err:
                return {'status': False, 'error': f'Erro ao obter conexão: {str(req_err)}'}
            
            except Exception as err:
                return {'status': False, 'error': f'Erro inesperado: {str(err)}'}
        
        # Retorna erro
        return {'status': False, 'error': f'{result.get('error')}'}
    
    def get_root_files(self, site_id):

        # Link de acesso a todos os arquivos na pasta raiz
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/children"
        response = requests.get(url=url, headers=self.headers) # Requisição para obter a raíz

        # Verificação se foi possível obter
        if response.status_code == 200:
            return response.json().get('value') # Retorna todos os dados

        # Retorna nada
        return None