resource "aws_s3_bucket_object" "etl" {
  bucket = aws_s3_bucket.artfacts.id
  key    = "etl/ingest_dados_publicos.py"
  acl    = "private"
  source = "../artfacts/etl/ingest_dados_publicos.py"
  etag   = filemd5("../artfacts/etl/ingest_dados_publicos.py")
}

resource "aws_s3_bucket_object" "etl_dm" {
  bucket = aws_s3_bucket.artfacts.id
  key    = "etl/ingest_dm.py"
  acl    = "private"
  source = "../artfacts/etl/ingest_dm.py"
  etag   = filemd5("../artfacts/etl/ingest_dm.py")
}

resource "aws_s3_bucket_object" "dag" {
  bucket = aws_s3_bucket.artfacts.id
  key    = "dags/nefesh_pipeline.py"
  acl    = "private"
  source = "../airflow/dags/nefesh_pipeline.py"
  etag   = filemd5("../airflow/dags/nefesh_pipeline.py")
}

resource "aws_s3_bucket_object" "install_sh" {
  bucket = aws_s3_bucket.artfacts.id
  key    = "ec2/install.sh"
  acl    = "private"
  source = "./install.sh"
  etag   = filemd5("./install.sh")
}

resource "aws_s3_bucket_object" "run_sh" {
  bucket = aws_s3_bucket.artfacts.id
  key    = "ec2/run.sh"
  acl    = "private"
  source = "./run.sh"
  etag   = filemd5("./run.sh")
}