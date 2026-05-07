import boto3
import uuid
import logging
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

import settings
from sns_utils import send_admin_alert

LOG_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), 'logs', 'automation.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_s3():
    try:
        s3 = boto3.client('s3', region_name=settings.AWS_REGION)
        random_id = str(uuid.uuid4())[:8]
        bucket_name = f"cloud-automation-{random_id}"

        print(f"Creating Bucket: {bucket_name}")
        if settings.AWS_REGION == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION}
            )

        print("Bucket Created Successfully")
        logging.info(f"S3 Bucket Created: {bucket_name}")

        send_admin_alert(
            subject="[AWS Automation] S3 Bucket Created",
            message=f"A new S3 bucket was created.\n\nBucket Name: {bucket_name}\nRegion: {settings.AWS_REGION}"
        )

        return bucket_name

    except Exception as e:
        print(f"Error creating S3: {e}")
        logging.error(f"Error creating S3: {str(e)}")
        return None

if __name__ == "__main__":
    create_s3()