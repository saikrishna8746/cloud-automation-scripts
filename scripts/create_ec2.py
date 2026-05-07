import boto3
import logging
import os
import uuid
import sys

# Ensure the scripts directory is in the path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

import settings
from sns_utils import send_admin_alert

LOG_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), 'logs', 'automation.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_instance():
    try:
        ec2 = boto3.resource('ec2', region_name=settings.AWS_REGION)
        random_id = str(uuid.uuid4())[:8]
        instance_name = f"automation-server-{random_id}"

        print(f"Creating EC2 Instance: {instance_name}...")
        instances = ec2.create_instances(
            ImageId=settings.EC2_AMI_ID,
            MinCount=1,
            MaxCount=1,
            InstanceType=settings.EC2_INSTANCE_TYPE,
            KeyName=settings.EC2_KEY_NAME,
            TagSpecifications=[
                {'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': instance_name}]}
            ]
        )

        instance = instances[0]
        print(f"EC2 Instance Created: {instance.id}")
        logging.info(f"EC2 Created | Name: {instance_name} | ID: {instance.id}")

        send_admin_alert(
            subject="[AWS Automation] EC2 Instance Created",
            message=f"A new EC2 instance was created.\n\nName: {instance_name}\nID: {instance.id}\nRegion: {settings.AWS_REGION}"
        )

        return instance.id

    except Exception as e:
        print(f"Error creating EC2: {e}")
        logging.error(f"Error creating EC2: {str(e)}")
        return None

if __name__ == "__main__":
    create_instance()