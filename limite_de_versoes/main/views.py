from django.shortcuts import render, redirect
from . import funcs

def form_screen(request):
    
    if request.method == 'GET':

        # Obtendo API do SharePoint e criando objeto
        sharepointObj = funcs.SharePoint()

        # Criando objeto do SharePoint
        result = sharepointObj.get_all_sites() # Obtendo todos os sites
        if result.get('status', False):
            
            # Obtem todos os dados dos sites
            all_sites = result.get('data')
            
            # Cria o contexto para página
            context = {
                'sites': all_sites
            }

            # Retorna os dados do contexto para a página
            return render(request, 'form.html', context)

        # Retorna o erro obtido
        return render(request, 'error.html', {'message': result.get('error')})

def process_data(request):
    if request.method == 'POST':
        return render(request, 'error.html', {'message': 'Não foi possível se conectar ao servidor'})