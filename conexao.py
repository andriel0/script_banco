from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import requests
import json
from tables import Base, Empenho, AgentePublico, Bens, Bens1, Empenho1
from decoder import LazyDecoder, clean_json
from importacoes import range_string, meses
from tables1 import Liquidacao, Base1, NotasPagamento, NotasFiscais, NotasEmpenho


mun = ['015', '027', '049', '061', '073', '075', '085', '087',
       '116', '123', '138', '149']

mun = ['004', '045', '061']

engine = create_engine("postgresql://postgres:postgres@localhost:5432/bens")
engine1 = create_engine("postgresql://postgres:Kael190606@167.99.227.128:5433/notas")

session = Session(engine)
session1 = Session(engine1)


def consume_api(api_r, table):
    table_dic = {
        'Empenho': Empenho1,
        'AgentePublico': AgentePublico,
        'Bens': Empenho1,
        'liquidacao': Liquidacao,
        'notas_pag': NotasPagamento,
        'notas_fis': NotasFiscais,
        'notas_emp': NotasEmpenho
    }

    try:
        # Clean and parse the API response
        api_cleaned = clean_json(api_r.text)  # Assuming `api_r` is a `requests.Response` object
        api_json = json.loads(api_cleaned, cls=LazyDecoder)
    except Exception as e:
        raise ConnectionError(f"Failed to clean or parse API data: {e}")

    # Extract data based on known API structure
    try:
        if 'data' in api_json and 'data' in api_json['data']:
            api_data = api_json['data']['data']
        elif 'rsp' in api_json and '_content' in api_json['rsp']:
            api_data = api_json['rsp']['_content']
        else:
            raise KeyError("Expected data structure not found in API response.")
    except Exception as e:
        raise ValueError(f"Error while extracting data from API response: {e}")

    # Insert data into the database
    try:
        for item in api_data:
            code_entry = table_dic[table](**item)  # Map JSON keys to the model
            session1.add(code_entry)
        session1.commit()
    except Exception as e:
        session1.rollback()
        raise RuntimeError(f"Failed to insert data into the database: {e}")


def consume_orgaos_api(api_r):
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

    lista = []
    for dic in api:
        lista.append(dic["codigo_orgao"])
    return lista


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
        elif table == 'notas_pag':
            try:
                for year in range(2017, 2025):
                    try:
                        api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/notas_pagamentos.json?'
                                                   f'codigo_municipio={m}&exercicio_orcamento={year}00')
                        consume_api(api_request, table)
                    except:
                        for month in meses:
                            try:
                                api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/notas_'
                                                           f'pagamentos.json?codigo_municipio={m}&exercicio_orcamento='
                                                           f'{year}00&data_referencia={year}{month}')
                                consume_api(api_request, table)
                            except:
                                print(f'Erro na {table} do município {m} e data de referência da liquidação {month/year}')
            except:
                print(f'Possível erro de API no município {m}')
        elif table == 'notas_fis':
            try:
                for year in range(2017, 2025):
                    try:
                        api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/notas_fiscais.json?'
                                                   f'codigo_municipio={m}&exercicio_orcamento={year}00')
                        consume_api(api_request, table)
                    except:
                        for month in meses:
                            try:
                                api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/notas_'
                                                           f'fiscais.json?codigo_municipio={m}&exercicio_orcamento='
                                                           f'{year}00&data_referencia={year}{month}')
                                consume_api(api_request, table)
                            except:
                                print(f'Erro na {table} do município {m} e data de referência da liquidação {month/year}')
            except:
                print(f'Possível erro de API no município {m}')
        elif table == 'notas_emp':
            try:
                for year in range(2017, 2025):
                    api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/orgaos.json?codigo_municipio'
                                               f'={m}&exercicio_orcamento={year}00')

                    orgaos = consume_orgaos_api(api_request)

                    print(year, m, orgaos)

                    for orgao in orgaos:
                        for month in meses:
                            try:
                                print(f'Mun: {m} em {month}/{year} - órgão {orgao}')
                                api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/notas_empenhos.'
                                                           f'json?codigo_municipio={m}&codigo_orgao={orgao}&data_'
                                                           f'referencia_empenho={year}{month}')
                                if api_request:
                                    consume_api(api_request, table)
                                else:
                                    print(f'Não deu no {m} em {month}/{year}')
                            except:
                                print(f'Erro na {table} do município {m} e data de referência do empenho {month / year}')
            except:
                print(f'Possível erro de API no município {m}')

            # import required module
            from playsound import playsound

            # for playing note.wav file
            playsound('mixkit-doorbell-tone-2864.wav')

# api_request = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/notas_empenhos.json?codigo_municipio'
#                            f'=012&codigo_orgao=06&data_referencia_empenho=202305')
# try:
#     consume_api(api_request, 'notas_emp')
# except:
#     raise ConnectionError('ERRO')

# Mun: 013 em 08/2017 - órgão 05
# Possível erro de API no município 013