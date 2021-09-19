resource "aws_s3_bucket" "raw_data" {
  bucket = "nefesh-raw-data"
  acl    = "private"

  tags = {
    PROJECT   = "NEFESH",
    AUTHOR    = "Daniela Muniz"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
resource "aws_s3_bucket_public_access_block" "raw_data" {
  bucket = aws_s3_bucket.raw_data.id

  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket" "stage_data" {
  bucket = "nefesh-stage-data"
  acl    = "private"

  tags = {
        PROJECT   = "NEFESH",
        AUTHOR    = "Daniela Muniz"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
resource "aws_s3_bucket_public_access_block" "stage_data" {
  bucket = aws_s3_bucket.stage_data.id

  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket" "trusted_data" {
  bucket = "nefesh-trusted-data"
  acl    = "private"

  tags = {
        PROJECT   = "NEFESH",
        AUTHOR    = "Daniela Muniz"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
resource "aws_s3_bucket_public_access_block" "trusted_data" {
  bucket = aws_s3_bucket.trusted_data.id

  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket" "artfacts" {
  bucket = "nefesh-artfacts"
  acl    = "private"

  tags = {
        PROJECT   = "NEFESH",
        AUTHOR    = "Daniela Muniz"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
resource "aws_s3_bucket_public_access_block" "artfacts" {
  bucket = aws_s3_bucket.artfacts.id

  block_public_acls   = true
  block_public_policy = true
}