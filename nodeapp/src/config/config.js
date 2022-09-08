export const config = {
  "dev": {
    "username": "postgres",
    "password": "Postgres12",
    "database": "softdev01",
    "host": "soft-dev.cixnnif6iavq.us-east-1.rds.amazonaws.com",
    "dialect": "postgres",
    "aws_region": "us-east-1",
    "aws_profile": "default",
    "aws_media_bucket": "udagram-ruttner-dev"
  },
  "jwt": {
    "secret": "secret"
  },
  "prod": {
    "username": "",
    "password": "",
    "database": "udagram_prod",
    "host": "",
    "dialect": "postgres"
  },
  "express": {
    "post": "",
    "host": ""
  }
}
