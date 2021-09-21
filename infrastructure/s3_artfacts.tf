resource "aws_s3_bucket_object" "etl" {
  bucket = aws_s3_bucket.artfacts.id
  key    = "etl/ingest_dados_publicos.py"
  acl    = "private"
  source = "../artfacts/etl/ingest_dados_publicos.py"
  etag   = filemd5("../artfacts/etl/ingest_dados_publicos.py")
}

resource "aws_s3_bucket_object" "dag" {
  bucket = aws_s3_bucket.artfacts.id
  key    = "dag/nefesh_pipeline.py"
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