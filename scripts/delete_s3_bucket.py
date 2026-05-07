import boto3
import logging
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

import settings
from sns_utils import send_admin_alert

LOG_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), 'logs', 'automation.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def delete_s3(bucket_name):
    try:
        s3 = boto3.client('s3', region_name=settings.AWS_REGION)

        print(f"Deleting Bucket: {bucket_name}")
        
        # Must empty bucket before deleting
        s3_resource = boto3.resource('s3', region_name=settings.AWS_REGION)
        bucket = s3_resource.Bucket(bucket_name)
        bucket.objects.all().delete()

        s3.delete_bucket(Bucket=bucket_name)

        print(f"Bucket Deleted Successfully: {bucket_name}")
        logging.info(f"S3 Bucket Deleted: {bucket_name}")

        send_admin_alert(
            subject="[AWS Automation] S3 Bucket Deleted",
            message=f"An S3 bucket was deleted.\n\nBucket Name: {bucket_name}\nRegion: {settings.AWS_REGION}"
        )

    except Exception as e:
        print(f"Error deleting S3: {e}")
        logging.error(f"Error deleting S3 {bucket_name}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        delete_s3(sys.argv[1])
    else:
        print("Please provide a bucket name")