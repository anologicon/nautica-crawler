import boto3
import os
from dotenv import load_dotenv

load_dotenv()

files_list = os.listdir('./data/parsed')
session = boto3.Session(profile_name=os.environ['AWS_PROFILE'])
client = session.client('s3')

for file in files_list:
    client.put_object(
        Body=f'./data/parsed/{file}',
        Bucket='nautica-crawler-data',
        Key=f'bronze/data/{file}'
    )