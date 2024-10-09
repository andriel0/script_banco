from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Empenho(Base):
    __tablename__ = 'empenho'
    id = Column(Integer, primary_key=True)
    codigo_municipio = Column(String)
    numero_registro_bem = Column(String)
    exercicio_orcamento = Column(String)
    codigo_orgao = Column(String)
    codigo_unidade = Column(String)
    data_emissao_empenho = Column(String)
    numero_nota_empenho = Column(String)
    data_referencia = Column(String)


class Empenho1(Base):
    __tablename__ = 'empenho1'
    id = Column(Integer, primary_key=True)
    codigo_municipio = Column(String)
    numero_registro_bem = Column(String)
    exercicio_orcamento = Column(String)
    codigo_orgao = Column(String)
    codigo_unidade = Column(String)
    data_emissao_empenho = Column(String)
    numero_nota_empenho = Column(String)
    data_referencia = Column(String)


class AgentePublico(Base):
    __tablename__ = 'agente'
    id = Column(Integer, primary_key=True)
    codigo_municipio = Column(String)
    exercicio_orcamento = Column(String)
    codigo_orgao = Column(String)
    codigo_unidade = Column(String)
    cpf_servidor = Column(String)
    codigo_ingresso = Column(String)
    codigo_vinculo = Column(String)
    numero_expediente_nomeacao = Column(String)
    codigo_expediente = Column(String)
    data_expediente = Column(String)
    codigo_amparo_legal = Column(String)
    numero_amparo_legal = Column(String)
    data_amparo_legal = Column(String)
    data_publicacao_amparo_legal = Column(String)
    data_posse = Column(String)
    numero_matricula = Column(String)
    situacao_funcional = Column(String)
    codigo_regime_juridico = Column(String)
    codigo_regime_previdencia = Column(String)
    codigo_ocupacao_cbo = Column(String)
    tipo_cargo = Column(String)
    valor_carga_horaria = Column(String)
    numero_dependentes = Column(String)
    data_referencia_agente_publico = Column(String)
    nome_servidor = Column(String)
    tipo_programa_social = Column(String)
    codigo_programa_social = Column(String)


class Bens(Base):
    __tablename__ = 'bens_municipios'
    id = Column(Integer, primary_key=True)
    codigo_municipio = Column(String)
    numero_registro_bem = Column(String)
    data_referencia_bem = Column(String)
    data_aquisicao_bem = Column(String)
    tipo_classificacao_bem = Column(String)
    tipo_natureza_bem = Column(String)
    status_baixado_bem = Column(String)
    descricao_bem1 = Column(String)
    descricao_bem2 = Column(String)


class Bens1(Base):
    __tablename__ = 'bens_municipios_r'
    id = Column(Integer, primary_key=True)
    codigo_municipio = Column(String)
    numero_registro_bem = Column(String)
    data_referencia_bem = Column(String)
    data_aquisicao_bem = Column(String)
    tipo_classificacao_bem = Column(String)
    tipo_natureza_bem = Column(String)
    status_baixado_bem = Column(String)
    descricao_bem1 = Column(String)
    descricao_bem2 = Column(String)