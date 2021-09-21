import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as fnc


# Argumentos
nome_tabela = sys.argv[1]
nome_db = sys.argv[2]

# Cria objeto da Spark Session
spark = (SparkSession.builder.appName(f"Ingestao da Tabela - {nome_tabela}")
    .config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory")
    .enableHiveSupport() 
    .getOrCreate()
)

# Cria banco de dados se nao existir
spark.sql(f"CREATE DATABASE IF NOT EXISTS {nome_db}")
spark.catalog.setCurrentDatabase(nome_db)

# Verifica schema da tabela
schema_tabela = ""
if (nome_tabela == "empresa"):
    schema_tabela = StructType ([
                    StructField('cnpj_basico', LongType()),
                    StructField('razao_social', StringType()),
                    StructField('natureza_juridica', LongType()),
                    StructField('qualificacao_responsavel', LongType()),
                    StructField('capital_social', DoubleType()), ## perguntar
                    StructField('porte_empresa', IntegerType()),  ##  array
                    StructField('ente_federativo_responsavel', StringType()) # aceita null
                    ])
elif (nome_tabela == "estabelecimento"):
    schema_tabela = StructType ([
                    StructField('cnpj_basico', LongType()),
                    StructField('cnpj_ordem', LongType()),
                    StructField('cnpj_dv', LongType()),
                    StructField('id_matriz_filial', IntegerType()), # array
                    StructField('nome_fantasia', StringType()),
                    StructField('situacao_cadastral', IntegerType()),  ## array
                    StructField('dt_situacao_cadastral', LongType()),
                    StructField('motivo_situacao_cadastral', LongType()),
                    StructField('nome_cidade_exterior', StringType()),
                    StructField('pais', LongType()),
                    StructField('dt_inicio_atividade', LongType()),
                    StructField('cnae_fiscal_principal', LongType()),
                    StructField('cnae_fiscal_secundaria', StringType()),
                    StructField('tipo_logradouro', StringType()),
                    StructField('logradouro', StringType()),
                    StructField('numero', StringType()),
                    StructField('complemento', StringType()),
                    StructField('bairro', StringType()),
                    StructField('cep', LongType()),
                    StructField('uf', StringType()),
                    StructField('municipio', LongType()),
                    StructField('ddd_1', IntegerType()),
                    StructField('telefone_1', LongType()),
                    StructField('ddd_2', IntegerType()),
                    StructField('telefone_2', LongType()),
                    StructField('ddd_fax', IntegerType()),
                    StructField('fax', LongType()),
                    StructField('correio_eletronico', StringType()),
                    StructField('situacao_especial', StringType()),
                    StructField('dt_situacao_especial', LongType())         
                    ])
elif (nome_tabela == "simples_mei"):
    schema_tabela = StructType ([
                    StructField('cnpj_basico', LongType()),
                    StructField('opcao_simples', StringType()), # array aceita null
                    StructField('dt_opcao_simples', LongType()),
                    StructField('dt_exclusao_simples', LongType()),
                    StructField('opcao_mei', StringType()), # array/aceita null
                    StructField('dt_opcao_mei', LongType()), 
                    StructField('dt_exclusao_mei', LongType())
                    ])
elif (nome_tabela == "cnae"):
    schema_tabela = StructType ([
                    StructField('codigo', LongType()),
                    StructField('descricao', StringType())
                    ])
elif (nome_tabela == "municipio"):
    schema_tabela = StructType ([
                    StructField('codigo', LongType()),
                    StructField('descricao', StringType())
                    ])
elif (nome_tabela == "natureza_juridica"):
    schema_tabela = StructType ([
                    StructField('codigo', LongType()),
                    StructField('descricao', StringType())
                    ])
elif (nome_tabela == "pais"):
    schema_tabela = StructType ([
                    StructField('codigo', LongType()),
                    StructField('descricao', StringType())
                    ])

# Leitura dos dados
dfOrigem = (
    spark.read.format("csv")
    .schema(schema_tabela)
    .option("header", False)
    .option("delimiter", ";")
    .option("encoding", "ISO-8859-1")
    .load(f"s3://nefesh-raw-data/dados_publicos/{nome_tabela}/")
)

# Gera os parquets e salva como tabela externa no glue
dfDestino = (
    dfOrigem
    .write
    .mode("overwrite")
    .format("parquet")
    .option("path", f"s3://nefesh-stage-data/dados_publicos/{nome_tabela}/")
    .saveAsTable(nome_tabela)
)
