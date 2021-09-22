from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.operators.emr_add_steps import EmrAddStepsOperator
from airflow.providers.amazon.aws.operators.emr_create_job_flow import EmrCreateJobFlowOperator
from airflow.providers.amazon.aws.operators.emr_terminate_job_flow import EmrTerminateJobFlowOperator
from airflow.providers.amazon.aws.sensors.emr_step import EmrStepSensor
from airflow.operators.dummy import DummyOperator

# Configurar as connections no UI do Airflow
# aws_default - Extra field: {"region_name": "us-east-2"}
# emr_default - Extra field: {"JobFlowRole":"EMR_EC2_DefaultRole","ServiceRole":"EMR_DefaultRole"}

def create_step(nome_tabela):
    STEP = [
        {
            'Name': f"ingest_{nome_tabela}",
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['spark-submit', '--master', 'yarn', '--deploy-mode', 'cluster',
                    '--name', f'Ingestao da tabela {nome_tabela}', 's3://nefesh-artfacts/etl/ingest_dados_publicos.py',
                    f'{nome_tabela}', 'nefesh_stage'
                ],
            },
        }
    ]
    return STEP

def create_step_dm(nome_tabela):
    STEP = [
        {
            'Name': f"ingest_{nome_tabela}",
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['spark-submit', '--master', 'yarn', '--deploy-mode', 'cluster',
                    '--name', f'Ingestao da tabela {nome_tabela}', 's3://nefesh-artfacts/etl/ingest_dm.py',
                    f'{nome_tabela}', 'nefesh_trusted'
                ],
            },
        }
    ]
    return STEP

JOB_FLOW_OVERRIDES = {
	"Name"                 : "EMR-Pipeline-NEFESH",
	"ServiceRole"          : "EMR_DefaultRole",
	"JobFlowRole"          : "EMR_EC2_DefaultRole",
	"VisibleToAllUsers"    : True,
	"LogUri"               : "s3://nefesh-raw-data/emr_logs/",
	"ReleaseLabel"         : "emr-6.1.0",
	"Instances"            : {
	    "InstanceGroups": [
	        {
	            "Name"         : "Master nodes",
	            "Market"       : "SPOT",
	            "InstanceRole" : "MASTER",
	            "InstanceType" : "m5.xlarge",
	            "InstanceCount": 1,
	        },
	        {
	            "Name"         : "Worker nodes",
	            "Market"       : "SPOT",
	            "InstanceRole" : "CORE",
	            "InstanceType" : "m5.xlarge",
	            "InstanceCount": 2,
	        }
	    ],
	    "KeepJobFlowAliveWhenNoSteps": True,
	    "TerminationProtected"       : False,
	    "Ec2KeyName"                 : "pipeline_key_pair",
	    "Ec2SubnetId"                : "subnet-c19e50aa"
	},
	"Applications"         : [
	    {"Name": "Spark"},
	    {"Name": "Hive"},
	    {"Name": "Livy"},
	],
	"Configurations"       : [
	    {
	        "Classification": "spark-env",
	        "Properties"    : {},
	        "Configurations": [{
	            "Classification": "export",
	            "Properties": {
	                "PYSPARK_PYTHON"        : "/usr/bin/python3",
	                "PYSPARK_DRIVER_PYTHON" : "/usr/bin/python3"
	            }
	        }]
	    },
	    {
	        "Classification": "spark-hive-site",
	        "Properties": {
	            "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
	        }
	    },
	    {
	        "Classification": "spark-defaults",
	        "Properties": {
	            "spark.submit.deployMode"   : "cluster",
	            "spark.speculation"         : "false",
	            "spark.sql.adaptive.enabled": "true",
	            "spark.serializer"          : "org.apache.spark.serializer.KryoSerializer"
	        }
	    },
	    {
	        "Classification": "spark",
	        "Properties": {
	            "maximizeResourceAllocation": "true"
	        }
	    }
	],
	"StepConcurrencyLevel" : 3,
}

with DAG(
    dag_id='nefesh_dados_publicos_dag',
    default_args={
        'owner': 'dmuniz',
    },
    dagrun_timeout=timedelta(hours=2),
    start_date=datetime(2021, 9, 20),
    schedule_interval='@monthly',
    tags=['dados publicos', 'cnpj'],
) as dag:

    # Inicia o Cluster
    start_cluster = EmrCreateJobFlowOperator(
        task_id='start_cluster',
        job_flow_overrides=JOB_FLOW_OVERRIDES,
        aws_conn_id='aws_default',
        emr_conn_id='emr_default',
    )

    # Task e Sensor da tabela empresa
    step_empresa = EmrAddStepsOperator(
        task_id='ingest_empresa',
        job_flow_id=start_cluster.output,
        aws_conn_id='aws_default',
        steps=create_step('empresa'),
    )
    wait_empresa = EmrStepSensor(
        task_id='wait_empresa',
        job_flow_id=start_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='ingest_empresa', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

     # Task e Sensor da tabela estabelecimento
    step_estabelecimento = EmrAddStepsOperator(
        task_id='ingest_estabelecimento',
        job_flow_id=start_cluster.output,
        aws_conn_id='aws_default',
        steps=create_step('estabelecimento'),
    )
    wait_estabelecimento = EmrStepSensor(
        task_id='wait_estabelecimento',
        job_flow_id=start_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='ingest_estabelecimento', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

    # Task e Sensor da tabela simples_mei
    step_simples_mei = EmrAddStepsOperator(
        task_id='ingest_simples_mei',
        job_flow_id=start_cluster.output,
        aws_conn_id='aws_default',
        steps=create_step('simples_mei'),
    )
    wait_simples_mei = EmrStepSensor(
        task_id='wait_simples_mei',
        job_flow_id=start_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='ingest_simples_mei', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

    # Task e Sensor da tabela cnae
    step_cnae = EmrAddStepsOperator(
        task_id='ingest_cnae',
        job_flow_id=start_cluster.output,
        aws_conn_id='aws_default',
        steps=create_step('cnae'),
    )
    wait_cnae = EmrStepSensor(
        task_id='wait_cnae',
        job_flow_id=start_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='ingest_cnae', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

    # Task e Sensor da tabela municipio
    step_municipio = EmrAddStepsOperator(
        task_id='ingest_municipio',
        job_flow_id=start_cluster.output,
        aws_conn_id='aws_default',
        steps=create_step('municipio'),
    )
    wait_municipio = EmrStepSensor(
        task_id='wait_municipio',
        job_flow_id=start_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='ingest_municipio', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

    # Task e Sensor da tabela natureza_juridica
    step_natureza = EmrAddStepsOperator(
        task_id='ingest_natureza_juridica',
        job_flow_id=start_cluster.output,
        aws_conn_id='aws_default',
        steps=create_step('natureza_juridica'),
    )
    wait_natureza = EmrStepSensor(
        task_id='wait_natureza_juridica',
        job_flow_id=start_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='ingest_natureza_juridica', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

    # Task e Sensor da tabela pais
    step_pais = EmrAddStepsOperator(
        task_id='ingest_pais',
        job_flow_id=start_cluster.output,
        aws_conn_id='aws_default',
        steps=create_step('pais'),
    )
    wait_pais = EmrStepSensor(
        task_id='wait_pais',
        job_flow_id=start_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='ingest_pais', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

    # Task e Sensor da tabela dm_empresa
    step_dm_empresa = EmrAddStepsOperator(
        task_id='ingest_dm_empresa',
        job_flow_id=start_cluster.output,
        aws_conn_id='aws_default',
        steps=create_step_dm('dm_empresa'),
    )
    wait_dm_empresa = EmrStepSensor(
        task_id='wait_dm_empresa',
        job_flow_id=start_cluster.output,
        step_id="{{ task_instance.xcom_pull(task_ids='ingest_dm_empresa', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

    # Finaliza o Cluster
    stop_cluster = EmrTerminateJobFlowOperator(
        task_id='stop_cluster',
        job_flow_id=start_cluster.output,
        aws_conn_id='aws_default',
    )

    nothing_1 = DummyOperator(
        task_id="nothing_1"
    )

    #step_adder >> step_checker >> stop_cluster
    start_cluster >> [step_empresa, step_estabelecimento, step_simples_mei, step_cnae, step_municipio, step_natureza, step_pais] >> nothing_1
    nothing_1 >> [wait_empresa, wait_estabelecimento, wait_simples_mei, wait_cnae, wait_municipio, wait_natureza, wait_pais] >> step_dm_empresa
    step_dm_empresa >> wait_dm_empresa >> stop_cluster