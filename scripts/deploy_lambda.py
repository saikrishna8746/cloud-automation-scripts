import boto3
import uuid
import time
import logging
import os
from sns_utils import send_admin_alert
import settings

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(
    os.path.dirname(SCRIPT_DIR),
    'logs',
    'automation.log'
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

lambda_client = boto3.client(
    'lambda',
    region_name=settings.AWS_REGION
)

# Generate random Lambda name
random_id = str(uuid.uuid4())[:8]

function_name = f"automation-lambda-{random_id}"

try:

    # Read Lambda ZIP package
    with open('lambda/lambda.zip', 'rb') as f:
        zipped_code = f.read()

    print(f"Creating Lambda Function: {function_name}")

    # Create Lambda
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.12',
        Role=settings.LAMBDA_EXECUTION_ROLE_ARN,
        Handler='lambda_function.lambda_handler',
        Code={
            'ZipFile': zipped_code
        },
        Timeout=30,
        Publish=True
    )

    print("Lambda Function Created Successfully")

    logging.info(
        f"Lambda Created | Name: {function_name}"
    )

    send_admin_alert(
        subject="[AWS Automation] Lambda Function Created",
        message=f"A new Lambda function was created.\n\nFunction Name: {function_name}\nRegion: ap-south-1"
    )

    print(f"Waiting {settings.WAIT_TIME_SECONDS} seconds before deletion...")

    time.sleep(settings.WAIT_TIME_SECONDS)

    # Delete Lambda
    lambda_client.delete_function(
        FunctionName=function_name
    )

    print(f"Lambda Function Deleted: {function_name}")

    logging.info(
        f"Lambda Deleted | Name: {function_name}"
    )

    send_admin_alert(
        subject="[AWS Automation] Lambda Function Deleted",
        message=f"A Lambda function was deleted.\n\nFunction Name: {function_name}\nRegion: ap-south-1"
    )

except Exception as e:

    print("Error:", e)

    logging.error(str(e))