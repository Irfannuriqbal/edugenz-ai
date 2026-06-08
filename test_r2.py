import os
import boto3
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "s3",
    endpoint_url=os.getenv("R2_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
    region_name="auto",
)

response = client.put_object(
    Bucket=os.getenv("R2_BUCKET_NAME"),
    Key="test.txt",
    Body="Hello from AWS EC2"
)

print(response)
