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

def delete_instance(instance_id):
    try:
        ec2 = boto3.resource('ec2', region_name=settings.AWS_REGION)
        instance = ec2.Instance(instance_id)

        print(f"Terminating EC2 Instance: {instance_id}...")
        instance.terminate()

        print(f"EC2 Instance Terminated: {instance_id}")
        logging.info(f"EC2 Terminated | ID: {instance_id}")

        send_admin_alert(
            subject="[AWS Automation] EC2 Instance Terminated",
            message=f"An EC2 instance was terminated.\n\nID: {instance_id}\nRegion: {settings.AWS_REGION}"
        )

    except Exception as e:
        print(f"Error terminating EC2: {e}")
        logging.error(f"Error terminating EC2 {instance_id}: {str(e)}")

def stop_instance(instance_id):
    try:
        ec2 = boto3.resource('ec2', region_name=settings.AWS_REGION)
        instance = ec2.Instance(instance_id)

        print(f"Stopping EC2 Instance: {instance_id}...")
        instance.stop()

        print(f"EC2 Instance Stopped: {instance_id}")
        logging.info(f"EC2 Stopped | ID: {instance_id}")

        send_admin_alert(
            subject="[AWS Automation] EC2 Instance Stopped",
            message=f"An EC2 instance was stopped.\n\nID: {instance_id}\nRegion: {settings.AWS_REGION}"
        )

    except Exception as e:
        print(f"Error stopping EC2: {e}")
        logging.error(f"Error stopping EC2 {instance_id}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        delete_instance(sys.argv[1])
    else:
        print("Please provide an instance ID")
