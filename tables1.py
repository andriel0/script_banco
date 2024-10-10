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


class NotasPagamento(Base1):
    __tablename__ = 'notas_pag'
    id = Column(Integer, primary_key=True)
    codigo_municipio = Column(String)
    exercicio_orcamento = Column(String)
    codigo_orgao = Column(String)
    codigo_unidade = Column(String)
    data_emissao_empenho = Column(String)
    numero_empenho = Column(String)
    numero_sub_empenho = Column(String)
    numero_nota_pagamento = Column(String)
    data_referencia = Column(String)
    nu_documento_caixa = Column(String)
    data_nota_pagamento = Column(String)
    valor_nota_pagamento = Column(String)
    valor_empenhado_a_pagar = Column(String)
    estado_de_estornado = Column(String)
    cpf_pagador = Column(String)
    nome_pagador = Column(String)


class NotasFiscais(Base1):
    __tablename__ = 'notas_fiscais'
    id = Column(Integer, primary_key=True)
    codigo_municipio = Column(String)
    exercicio_orcamento = Column(String)
    codigo_orgao = Column(String)
    codigo_unidade = Column(String)
    data_emissao_empenho = Column(String)
    numero_empenho = Column(String)
    data_liquidacao = Column(String)
    tipo_nota_fiscal = Column(String)
    numero_nota_fiscal = Column(String)
    data_referencia = Column(String)
    numero_serie_selo_transito = Column(String)
    numero_selo_transito = Column(String)
    numero_serie = Column(String)
    numero_formulario = Column(String)
    data_limite = Column(String)
    cgf_emitente = Column(String)
    data_emissao = Column(String)
    valor_liquido = Column(String)
    valor_desconto = Column(String)
    valor_bruto = Column(String)
    valor_aliquota_iss = Column(String)
    valor_base_calculo_iss = Column(String)
    tipo_emissao = Column(String)
    numero_protocolo_autenticacao = Column(String)
