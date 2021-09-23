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
    .config("spark.default.parallelism", "12") #qtas tasks o spark roda em paralelo
    .config("spark.dynamicAllocation.minExecutors","4") # worker
    .config("spark.dynamicAllocation.maxExecutors", "8") # worker
    .enableHiveSupport() 
    .getOrCreate()
)
sqls = {}
sqls["dm_empresa"] = """
SELECT
    emp.razao_social,
    emp.natureza_juridica,
    emp.qualificacao_responsavel,
    -- Substituir a , por . para tratar como decimal
    cast(regexp_replace(emp.capital_social,',','.') as decimal(16,2)) as capital_social,
    emp.porte_empresa,
    emp.ente_federativo_responsavel,
    est.*,
    mun.descricao as desc_municipio,
    pai.descricao as desc_pais,
    nat.descricao as desc_natureza_juridica,
    sim.opcao_simples,
    sim.dt_opcao_simples,
    sim.dt_exclusao_simples,
    sim.opcao_mei,
    sim.dt_opcao_mei,
    sim.dt_exclusao_mei,
    cna.descricao as desc_cnae_principal,
    substr(cast(est.dt_situacao_cadastral as string), 1, 4) as ano_situacao_cadastral,
    substr(cast(est.dt_situacao_cadastral as string), 5, 2) as mes_situacao_cadastral
FROM nefesh_stage.empresa as emp
    LEFT JOIN nefesh_stage.estabelecimento as est ON (emp.cnpj_basico = est.cnpj_basico)
    LEFT JOIN nefesh_stage.municipio as mun ON (mun.codigo = est.municipio)
    LEFT JOIN nefesh_stage.pais as pai ON (pai.codigo = est.pais)
    LEFT JOIN nefesh_stage.natureza_juridica as nat ON (nat.codigo = emp.natureza_juridica)
    LEFT JOIN nefesh_stage.simples_mei as sim ON (sim.cnpj_basico = est.cnpj_basico)
    LEFT JOIN nefesh_stage.cnae as cna ON (cna.codigo = est.cnae_fiscal_principal)
"""
sqls["dm_cnpj_por_cnae"] = """
WITH cte_cnae AS (
    SELECT 
        cnpj_basico, concat_ws(',', cast(cnae_fiscal_principal as varchar), cnae_fiscal_secundaria) as codigo_cnae
    FROM nefesh_trusted.dm_empresa
), cte_cnpj_cnae AS (
    SELECT cnpj_basico, value as cnae
    FROM cte_cnae
    CROSS JOIN UNNEST(split(cte_cnae.codigo_cnae, ',')) as x(value)
)
SELECT 
    cnpj.*,
    cn.descricao as desc_cnae
FROM cte_cnpj_cnae as cnpj
INNER JOIN nefesh_stage.cnae as cn ON (cnpj.cnae=cast(cn.codigo as varchar))
"""


# Cria banco de dados se nao existir
spark.sql(f"CREATE DATABASE IF NOT EXISTS {nome_db}")
spark.catalog.setCurrentDatabase(nome_db)

# Leitura dos dados
dfOrigem = spark.sql(sqls[nome_tabela])

# Gera os parquets e salva como tabela externa no glue
dfDestino = (
    dfOrigem
    .write
    .mode("overwrite")
    .format("parquet")
    .option("path", f"s3://nefesh-trusted-data/dados_publicos/{nome_tabela}/")
    .option("parquet.block.size", 128 * 1024 * 1024)
    .saveAsTable(nome_tabela)
)



