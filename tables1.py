from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base1 = declarative_base()


class Liquidacao(Base1):
    __tablename__ = 'liquidacoes'
    id = Column(Integer, primary_key=True)
    codigo_municipio = Column(String)
    exercicio_orcamento = Column(String)
    codigo_orgao = Column(String)
    codigo_unidade = Column(String)
    data_emissao_empenho = Column(String)
    numero_empenho = Column(String)
    data_liquidacao = Column(String)
    data_referencia_liquidacao = Column(String)
    nome_responsavel_liquidacao = Column(String)
    numero_sub_empenho_liquidacao = Column(String)
    valor_liquidado = Column(String)
    estado_de_estorno = Column(String)
    estado_folha = Column(String)
    cpf_responsavel_liquidacao = Column(String)
