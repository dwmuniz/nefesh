import sys
from pyspark.sql import SparkSession
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

# Leitura dos dados
dfOrigem = (
    spark.read.format("csv")
    .option("inferSchema", True)
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
