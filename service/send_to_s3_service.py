import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

s3_client = boto3.client("s3", region_name=os.getenv("REGION"))
BUCKET_NAME = os.getenv("BUCKET_NAME")


def save_to_s3(file_data: dict, pasta_destino: str):
    try:
        filename = file_data["filename"]
        content = file_data["content"]
        key = f"{pasta_destino}/{filename}"

        s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=content)

        s3_url = f"https://{BUCKET_NAME}.s3.{os.getenv('REGION')}.amazonaws.com/{key}"
        return s3_url

    except (NoCredentialsError, PartialCredentialsError):
        raise Exception("Credenciais inválidas para o S3.")
    except Exception as e:
        raise Exception(f"Erro ao salvar no S3: {str(e)}")

