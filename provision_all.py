import sys
import os
import time

# Add scripts directory to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from create_ec2 import create_instance
from create_s3_bucket import create_s3
from create_lambda import create_lambda
from state_utils import update_state
import settings
import destroy_all

def main():
    print("=======================================")
    print("   Starting Cloud Automation Provisioning")
    print("=======================================\n")

    # 1. Provision EC2
    print("--> Step 1: Provisioning EC2 Instance")
    instance_id = create_instance()
    if instance_id:
        update_state('ec2_instance_id', instance_id)
    print("")

    # 2. Provision S3
    print("--> Step 2: Provisioning S3 Bucket")
    bucket_name = create_s3()
    if bucket_name:
        update_state('s3_bucket_name', bucket_name)
    print("")

    # 3. Provision Lambda
    print("--> Step 3: Provisioning Lambda Function")
    lambda_name = create_lambda()
    if lambda_name:
        update_state('lambda_function_name', lambda_name)
    print("")

    print("=======================================")
    print("   Provisioning Complete!")
    print("   Resource IDs have been saved to state.json")
    print("=======================================\n")

    print(f"Waiting {settings.WAIT_TIME_SECONDS} seconds before automatic teardown...")
    time.sleep(settings.WAIT_TIME_SECONDS)
    print("")

    # Automatically call the destroy script
    destroy_all.main()

if __name__ == "__main__":
    main()
