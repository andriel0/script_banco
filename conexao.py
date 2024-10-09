from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import requests
import json
from tables import Base, Empenho, AgentePublico, Bens, Bens1, Empenho1
from decoder import LazyDecoder
from importacoes import range_string, meses
from tables1 import Liquidacao, Base1


mun = ['015', '027', '049', '061', '073', '075', '085', '087',
       '116', '123', '138', '149']

mun = ['004', '045', '061']

engine = create_engine("postgresql://postgres:postgres@localhost:5432/bens")
engine1 = create_engine("postgresql://postgres:Kael190606@167.99.227.128:5433/notas")

session = Session(engine)
session1 = Session(engine1)


def consume_api(api_r, table):
    table_dic = {'Empenho':Empenho1, 'AgentePublico':AgentePublico, 'Bens':Empenho1, 'liquidacao':Liquidacao}
    try:
        try:
            api_json = api_r.json()
        except:
            api_json = api_r.json(cls=LazyDecoder)

        try:
            api = api_json['data']['data']
        except:
            api = api_json['rsp']['_content']
    except:
        raise ConnectionError('API FORA DO AR')

    for item in api:
        code_entry = table_dic[table](**item)
        session1.add(code_entry)

    session1.commit()


def povoar_tabela(table):
    ano = ''
    mes = ''
    for m in mun:
        if table == 'Empenho':
            try:
                try:
                    api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/empenhos_bens.json?codigo_municipio={m}')
                    consume_api(api_request, table)
                except:
                    for year in range(2009, 2024):
                        for mon in range(1, 13):
                            if mon < 10:
                                month = '0' + str(mon)
                            else:
                                month = str(mon)
                            ano = year
                            mes = month
                            try:
                                api_request = requests.get(
                                    f'https://api.tce.ce.gov.br/index.php/sim/1_0/empenhos_bens.json?'
                                    f'codigo_municipio={m}&data_referencia={str(year)}{month}')
                                if api_request:
                                    consume_api(api_request, table)
                            except:
                                print(f'ERRO no município {m} de {mes}/{ano}')

            except:
                pass
        elif table == 'Bens':
            try:
                api_request = requests.get(
                    f'https://api-dados-abertos.tce.ce.gov.br/empenhos_bens?codigo_municipio={m}&'
                    f'quantidade=100&deslocamento=0')
                if api_request:
                    try:
                        try:
                            api_json = api_request.json()
                        except:
                            api_json = api_request.json(cls=LazyDecoder)

                    except:
                        print('Erro ao selecionar tamanho')
            except:
                pass
            total = api_json['data']['total']
            print(total)
            for l in range(0, total+1, 100):
                try:
                    api_dif = requests.get(
                        f'https://api-dados-abertos.tce.ce.gov.br/empenhos_bens?codigo_municipio={m}&'
                        f'quantidade=100&deslocamento={l}')
                    if api_dif:
                        consume_api(api_dif, table)
                    print(l)
                except:
                    print(f'ERRO no município {m} de deslocamento {l}')
        else:
            try:
                for year in range(2009, 2024):
                    ano = year
                    try:
                        api_request = requests.get(
                            f'https://api.tce.ce.gov.br/index.php/sim/1_0/agentes_publicos.json?codigo_municipio={m}'
                            f'&exercicio_orcamento={year}00')
                        if api_request:
                            consume_api(api_request, table)
                    except:
                        print(f'ERRO no {m} de {ano}')

            except:
                pass


def povoar_tabela1(table):
    for m in range_string:
        if table == 'liquidacao':
            try:
                for year in range(2017, 2025):
                    try:
                        api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/liquidacoes.json?'
                                                   f'codigo_municipio={m}&exercicio_orcamento={year}00')
                        consume_api(api_request, table)
                    except:
                        for month in meses:
                            try:
                                api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/liquidacoes.json?'
                                                           f'codigo_municipio={m}&exercicio_orcamento={year}00&data_'
                                                           f'referencia_liquidacao={year}{month}')
                                consume_api(api_request, table)
                            except:
                                print(f'Erro na {table} do município {m} e data de referência da liquidação {month/year}')
            except:
                print('Possível erro de API')