import boto3
import logging
import os
import time
import uuid
import settings
from sns_utils import send_admin_alert

print("Script Started")

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

try:

    # Use AMI ID from settings
    ec2 = boto3.resource(
        'ec2',
        region_name=settings.AWS_REGION
    )

    # Generate random EC2 instance name
    random_id = str(uuid.uuid4())[:8]

    instance_name = f"automation-server-{random_id}"

    print(f"Generated Random Name: {instance_name}")

    print("Creating EC2 Instance...")

    instances = ec2.create_instances(
        ImageId=settings.EC2_AMI_ID,
        MinCount=1,
        MaxCount=1,
        InstanceType=settings.EC2_INSTANCE_TYPE,
        KeyName=settings.EC2_KEY_NAME,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    },
                ]
            },
        ]
    )

    instance = instances[0]

    print(f"EC2 Instance Created: {instance.id}")

    logging.info(
        f"EC2 Created | Name: {instance_name} | ID: {instance.id}"
    )

    send_admin_alert(
        subject="[AWS Automation] EC2 Instance Created",
        message=f"A new EC2 instance was created.\n\nName: {instance_name}\nID: {instance.id}\nRegion: ap-south-1"
    )

    print("Waiting for instance to enter running state...")

    instance.wait_until_running()

    print("Instance is now running.")

    print(f"Waiting {settings.WAIT_TIME_SECONDS} seconds before termination...")

    time.sleep(settings.WAIT_TIME_SECONDS)

    instance.terminate()

    print(f"EC2 Instance Terminated: {instance.id}")

    logging.info(
        f"EC2 Terminated | Name: {instance_name} | ID: {instance.id}"
    )

    send_admin_alert(
        subject="[AWS Automation] EC2 Instance Terminated",
        message=f"An EC2 instance was terminated.\n\nName: {instance_name}\nID: {instance.id}\nRegion: ap-south-1"
    )

except Exception as e:

    print("Error:", e)

    logging.error(str(e))