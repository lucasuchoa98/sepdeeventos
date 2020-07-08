from celery import shared_task
from django.shortcuts import render, redirect
from django.core import serializers

@shared_task
def process_file_task(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        upload = request.FILES['file']
        workbook = pd.ExcelFile(upload.temporary_file_path())
        dfs = {sheet: workbook.parse(sheet) for sheet in workbook.sheet_names}
        df = dfs['Planilha1']
        deltae = float(request.POST.get('deltae'))
        if request.POST.get('ptot') == '':
            ptot = 0
        else:
            ptot = float(request.POST.get('ptot'))

        if request.POST.get('imed') == '':
            imed = 0
        else:
            imed = float(request.POST.get('imed'))

        if request.POST.get('deltat') == '':
            deltat = 0
        else:
            deltat = float(request.POST.get('deltat'))

        evento = objeto(deltae=deltae, df=df, ptot=ptot, imed=imed, deltat=deltat)
        evento.def_eventos()
        n_eventos = len(evento.dframe)

        if ptot != 0:
            evento.sel_by_ptot()
        
        if imed != 0:
            evento.sel_by_imed()

        if deltat != 0:
            evento.discretizando()
        big_df = pd.DataFrame()

        for i in evento.dframe.keys():
            top_row = pd.Series(['evento:',i+1])
            ndf = evento.dframe[i]
            
            arow = pd.DataFrame([top_row])
            result = pd.concat([arow,ndf],ignore_index= True)
            big_df = big_df.append(result, ignore_index= True)
            result = pd.DataFrame()

        big_df.to_excel('evento_separados.xlsx',sheet_name='planilha1')
        modelo_instance = Evento()

        with open('evento_separados.xlsx', 'rb') as excel:
            modelo_instance.upload.save('evento_separados.xlsx',File(excel))
        
        endereco = modelo_instance.upload.url
        
        n_eventos_filtered = len(evento.dframe)
        keys = evento.dframe.keys()
        #grafico = evento.grafico(0)
        
        #'grafico': grafico,
        context = {'evento':evento,
            'n_eventos':n_eventos,
            'n_eventos_filtered':n_eventos_filtered,
            'keys':keys,
            'endereco':endereco
            }
    return context