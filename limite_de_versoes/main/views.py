from django.shortcuts import render
from . import funcs

def form_screen(request):
    
    # Criando objeto do token de acesso
    tokenObj = funcs.AccessToken('e6921540-6b5e-41b4-b82d-9185b4225bcb', '80045d75-bc0e-4407-9a31-62b30df67338', 'RiU8Q~IFPdREqoGU2DAuln3iDDSEXQIBZNLzjc3O')

    # Obtendo token de acesso
    access_token, headers = tokenObj.get_access_token()
    if access_token is None:
        return render(request, 'error.html', {'message': 'Não foi possível obter o token de acesso'})

    # Criando objeto do SharePoint
    sharepointObj = funcs.SharePoint(access_token=access_token, headers=headers)
    all_sites = sharepointObj.get_all_sites() # Obtendo todos os sites

    # Verificação se foi possível obter todos os sites
    if all_sites is None:
        return render(request, 'error.html', {'message': 'Não foi possível obter os sites'})

    # Formatação dos dados para envio ao servidor
    context = {'sites': all_sites}
    
    # Obtendo todos os sites do SharePoint
    return render(request, 'form.html', context)