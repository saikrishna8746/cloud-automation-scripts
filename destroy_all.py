import sys
import os

# Add scripts directory to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from delete_ec2 import delete_instance
from delete_s3_bucket import delete_s3
from delete_lambda import delete_lambda
from state_utils import load_state, clear_state

def main():
    print("=======================================")
    print("   Starting Cloud Automation Teardown")
    print("=======================================\n")

    state = load_state()

    if not state:
        print("No state found in state.json. Nothing to destroy.")
        return

    # 1. Destroy EC2
    instance_id = state.get('ec2_instance_id')
    if instance_id:
        print(f"--> Step 1: Destroying EC2 Instance ({instance_id})")
        delete_instance(instance_id)
        print("")
    else:
        print("--> Step 1: No EC2 Instance found in state.\n")

    # 2. Destroy S3
    bucket_name = state.get('s3_bucket_name')
    if bucket_name:
        print(f"--> Step 2: Destroying S3 Bucket ({bucket_name})")
        delete_s3(bucket_name)
        print("")
    else:
        print("--> Step 2: No S3 Bucket found in state.\n")

    # 3. Destroy Lambda
    lambda_name = state.get('lambda_function_name')
    if lambda_name:
        print(f"--> Step 3: Destroying Lambda Function ({lambda_name})")
        delete_lambda(lambda_name)
        print("")
    else:
        print("--> Step 3: No Lambda Function found in state.\n")

    # Clear state after successful teardown
    clear_state()

    print("=======================================")
    print("   Teardown Complete!")
    print("   state.json has been cleared.")
    print("=======================================")

if __name__ == "__main__":
    main()
