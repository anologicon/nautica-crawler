import boto3
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

files_list = os.listdir('./data/parsed/details')
session = boto3.Session(profile_name=os.environ['AWS_PROFILE'])
client = session.client('s3')

for file in files_list:
    client.put_object(
        Body=f'./data/parsed/details/{file}',
        Bucket='nautica-crawler-data-bronze',
        Key=f'details/ingest_date_utc={datetime.utcnow()}/{file}'
    )