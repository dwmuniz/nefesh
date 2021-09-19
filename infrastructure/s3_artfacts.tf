resource "aws_s3_bucket_object" "etl" {
  bucket = aws_s3_bucket.artfacts.id
  key    = "etl/ingest_dados_publicos.py"
  acl    = "private"
  source = "../artfacts/etl/ingest_dados_publicos.py"
  etag   = filemd5("../artfacts/etl/ingest_dados_publicos.py")
}