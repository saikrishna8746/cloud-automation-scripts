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

def delete_lambda(function_name):
    try:
        lambda_client = boto3.client('lambda', region_name=settings.AWS_REGION)

        print(f"Deleting Lambda Function: {function_name}...")
        lambda_client.delete_function(FunctionName=function_name)

        print(f"Lambda Function Deleted: {function_name}")
        logging.info(f"Lambda Deleted | Name: {function_name}")

        send_admin_alert(
            subject="[AWS Automation] Lambda Function Deleted",
            message=f"A Lambda function was deleted.\n\nFunction Name: {function_name}\nRegion: {settings.AWS_REGION}"
        )

    except Exception as e:
        print(f"Error deleting Lambda: {e}")
        logging.error(f"Error deleting Lambda {function_name}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        delete_lambda(sys.argv[1])
    else:
        print("Please provide a function name")
