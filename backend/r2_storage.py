import os
import boto3

def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("R2_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
        region_name="auto",
    )

def upload_file_to_r2(local_path, object_name):
    client = get_r2_client()

    client.upload_file(
        local_path,
        os.getenv("R2_BUCKET_NAME"),
        object_name
    )

    return True
