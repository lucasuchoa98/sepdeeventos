# PIBIC19

Este repositório é referente ao aplicativo desenvolvido durante o ciclo do PIBIC 2019/20 orientado pelo Professor Marllus Gustavo da Universidade Federal de Alagoas.


Ao clonar o repositorio:

- Atente-se aos requirimets.txt

para instalar via [pip](https://pip.pypa.io/en/stable/) é so abrir o cmd e:

```bash
pip install -r requirements.txt
```
Feito isso, lembre-se de:
- atualizar o caminho da planilha com os dados de chuva que você deseja separar.

Por exemplo:

arq = r"<caminho_da_planilha.xlsx"

Que ficaria assim

arq = r"C:\Users\Lucas\Desktop\PIBIC19_20\dados\Plu_trincheira.xlsx"

Então, certifique-se que sua planilha contenha apenas 3 colunas, com a **primeira linha** contendo:


        | Sydney    |    1    | MLD144 |
        |25/05/2016	|02:21:00	|  0,20  |
        |    .      |    .    |   .    |
        |    .      |    .    |   .    |
        |    .      |    .    |   .    |


-------------

Após essas adequações especiais, um exemplo de utilização do script a partir do power shell ou prompt de comando - no mesmo diretorio do arquivo script.py:

- Primeiro você deve importar nosso modulo:

from script import Evento
  
- Então você deve instanciar o nosso evento, aqui você vai definir os parametros que
serão utilizados para para definir e filtrar os eventos.

- deltae é o tempo (min) entre dados para que seja considerado um novo evento.

- ptot é a precipitação total minima (mm) para que o evento seja considerado valido.

- imed é a intensidade média minima (mm/h) para que o evento seja considerado valido.

- deltat é o tempo (min) que o evento será dicretizado.
  
evento = Evento(deltae=60,ptot=5,imed=3,deltat=10)

evento.def_eventos()

evento.sel_by_ptot()

evento.sel_by_imed()
 
Agora, o evento já foi instanciado e já foi filtrado, e você pode fazer algumas coisas com ele, por exemplo:

- Se você quiser as keys (chaves) dos seus eventos, então:

evento.dframe.keys()

- Se você deseja saber qual foi o número de eventos selecionados:

numero = len(evento.dframe.keys())

print(numero)


- Se você desejar discretizar um evento, então:

evento.discretizando()
  
- Se deseja obter o gráfico (x=data,y=precipitação):

evento.grafico(key)
  

Duvidas? Entre em contato comigo pelo email lucasuchoalg@gmail.com
