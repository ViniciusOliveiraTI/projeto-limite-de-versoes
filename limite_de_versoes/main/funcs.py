import requests

# Criando Objeto para obter o token de acesso
class AccessToken:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        # Todas as variáveis necessárias
        self.tenant_id, self.client_id, self.client_secret = tenant_id, client_id, client_secret
    
    # Método para obter token de acesso
    def get_access_token(self):
        
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

        # Validando token
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            headers = {'Authorization': f'Bearer {access_token}'}
            return access_token, headers  # Retorna o token de acesso
        return None, None

# Objeto SharePoint para operações relacionadas
class SharePoint:
    def __init__(self, access_token: str, headers: dict):

        # Variáveis necessárias
        self.access_token = access_token    
        self.headers = headers

    # Método para listar todos os sites do SharePoint
    def get_all_sites(self):
    
        url = 'https://graph.microsoft.com/v1.0/sites?search=*' # URL que encontra todos os sites

        # Solicitação de conexão com a API
        response = requests.get(url, headers=self.headers)

        # Verificação se foi possível se conectar
        if response.status_code == 200:
            sites = response.json().get('value')
            return sites
        return None