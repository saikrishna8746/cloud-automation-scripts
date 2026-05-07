import boto3
import uuid
import logging
import os
import sys
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

import settings
from sns_utils import send_admin_alert

LOG_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), 'logs', 'automation.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_lambda():
    try:
        lambda_client = boto3.client('lambda', region_name=settings.AWS_REGION)
        random_id = str(uuid.uuid4())[:8]
        function_name = f"automation-lambda-{random_id}"

        lambda_dir = os.path.join(os.path.dirname(SCRIPT_DIR), 'lambda')
        zip_path = os.path.join(lambda_dir, 'lambda.zip')
        py_path = os.path.join(lambda_dir, 'lambda_function.py')

        # Automatically create the zip file
        with zipfile.ZipFile(zip_path, 'w') as z:
            z.write(py_path, arcname='lambda_function.py')

        with open(zip_path, 'rb') as f:
            zipped_code = f.read()

        print(f"Creating Lambda Function: {function_name}...")
        lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.12',
            Role=settings.LAMBDA_EXECUTION_ROLE_ARN,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zipped_code},
            Timeout=30,
            Publish=True
        )

        print("Lambda Function Created Successfully")
        logging.info(f"Lambda Created | Name: {function_name}")

        send_admin_alert(
            subject="[AWS Automation] Lambda Function Created",
            message=f"A new Lambda function was created.\n\nFunction Name: {function_name}\nRegion: {settings.AWS_REGION}"
        )

        return function_name

    except Exception as e:
        print(f"Error creating Lambda: {e}")
        logging.error(f"Error creating Lambda: {str(e)}")
        return None

if __name__ == "__main__":
    create_lambda()
