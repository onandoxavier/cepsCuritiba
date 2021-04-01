import pandas as pd
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

df = pd.DataFrame()

COLUNAS = [
    'BAIRRO',
    'CEP',
    'LOGRADOURO'
]

df = pd.DataFrame(columns=COLUNAS)

url = 'https://cepbrasil.org/parana/curitiba/'
req = requests.get(url)
if req.status_code == 200:
    print('Requisição bem sucedida!')
    content = req.content

soup = BeautifulSoup(content, 'html.parser')
listaBairros = soup.find_all("a", {"class": "box"})
#listaTeste = listaBairros[:1]

for e in listaBairros:
    bairro = f'{e.get("href")}'
    req = requests.get(f'{url}{bairro}')
    if req.status_code == 200:
        print('Requisição bairro bem sucedida!')
        contentBairro = req.content

    soupBairro = BeautifulSoup(contentBairro, 'html.parser')
    listaCeps = soupBairro.find_all("h4", {"class": "title"})
    for rua in listaCeps:
        value = rua.get_text()
        cep = f'{value[4:9]}{value[10:12]}'
        logradouro = f'{value[15:]}'
        df = df.append({'BAIRRO': bairro, 'CEP': cep, 'LOGRADOURO': unidecode(logradouro).strip().upper()}, ignore_index=True)

#df.to_csv(r'ceps_curitiba.csv', sep=';', index=False)
#print(df)


