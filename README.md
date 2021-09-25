# NEFESH

> Esse repositório foi usado para o desafio Challenge Women da A3 Data, na área de Engenharia de Dados.

<code><img  height="20"  src="https://img.shields.io/badge/Git-F05032?style=plastic&logo=git&logoColor=white"/></code>
<code><img  height="20"  src="https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white"/></code>
<code><img  height="20"  src="https://img.shields.io/badge/Python-3776AB?style=plastic&logo=python&logoColor=white"/></code>
<code><img  height="20"  src="https://img.shields.io/badge/Airflow-017CEE?style=plastic&logo=Apache%20Airflow&logoColor=white"/></code>
<code><img  height="20"  src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white"/></code>
<code><img  height="20"  src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/></code>

## Requerimentos
  
* Uma conta na Amazon AWS (http://aws.amazon.com)
* Algum conhecimento em Apache Airflow (https://airflow.apache.org)

## Setup da Implantação

O primeiro passo foi fazer uma merge request na branch main do git. Em seguida o Terraform se encarregará de de criar toda a infra-estrutura na AWS (buckets necessários; máquina EC2).

Após a disponibilização da EC2, conectar via ssh e executar os seguinte comandos para a disponibilização do Docker: 
```sh
curl -o /home/ubuntu/install.sh https://nefesh-artfacts.s3.us-east-2.amazonaws.com/ec2/install.sh 
chmod +x /home/ubuntu/install.sh
./home/ubuntu/install.sh
```

Após a instalação dos pacotes e Docker, deslogue-se e logue-se novamente na EC2 para o uso do mesmo. Em seguida execute os seguintes comando para instalar rodar o container do Apache Airflow e copiar a DAG necessária para o uso da pipeline:
```sh
curl -o /home/ubuntu/run.sh https://nefesh-artfacts.s3.us-east-2.amazonaws.com/ec2/run.sh
chmod +x /home/ubuntu/run.sh
./home/ubuntu/run.sh
```

## Uso 

Para acessar a UI do  Apache Airflow, basta copiar o endpoint público da máquina EC2 e acessar pela porta 8080, exemplo: http://ec2-4-123-54-39.us-east-2.compute.amazonaws.com:8080/

Usuário padrão: **admin**
Senha padrão: **admin**

Para a análise de dados, foi utilizado um Jupyter Notebook, acessando diretamente o Athena. Para essa possibilidade, instale a biblioteca *PyAthena* através do *pip*.

## Sobre Mim

Daniela Muniz

[![Github Badge](https://img.shields.io/badge/-Github-000?style=flat-square&logo=Github&logoColor=white&link=https://github.com/dwmuniz)](https://github.com/dwmuniz)
