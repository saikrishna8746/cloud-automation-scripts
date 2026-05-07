import argparse
import sys
import os

# Add scripts directory to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from create_ec2 import create_instance
from create_s3_bucket import create_s3
from create_lambda import create_lambda
from delete_ec2 import delete_instance, stop_instance
from delete_s3_bucket import delete_s3
from delete_lambda import delete_lambda
from state_utils import update_state

def main():
    parser = argparse.ArgumentParser(description="Cloud Automation CLI Manager")
    parser.add_argument('action', choices=['create', 'stop', 'terminate', 'delete'], help="Action to perform")
    parser.add_argument('resource_type', choices=['ec2', 's3', 'lambda'], help="Type of resource")
    parser.add_argument('resource_id', nargs='?', help="The ID or Name of the specific resource (Required for stop/terminate/delete)")

    args = parser.parse_args()

    if args.action in ['stop', 'terminate', 'delete'] and not args.resource_id:
        print(f"Error: You must provide a resource_id to {args.action} a {args.resource_type}.")
        sys.exit(1)

    print("=======================================")
    if args.action == 'create':
        print(f"   Executing: {args.action.upper()} on {args.resource_type.upper()}")
    else:
        print(f"   Executing: {args.action.upper()} on {args.resource_type.upper()} ({args.resource_id})")
    print("=======================================\n")

    if args.resource_type == 'ec2':
        if args.action == 'create':
            instance_id = create_instance()
            if instance_id:
                update_state('ec2_instance_id', instance_id)
                print(f"-> Saved ID {instance_id} to state.json")
        elif args.action == 'stop':
            stop_instance(args.resource_id)
        elif args.action in ['terminate', 'delete']:
            delete_instance(args.resource_id)

    elif args.resource_type == 's3':
        if args.action == 'create':
            bucket_name = create_s3()
            if bucket_name:
                update_state('s3_bucket_name', bucket_name)
                print(f"-> Saved Name {bucket_name} to state.json")
        elif args.action == 'stop':
            print("Error: You cannot 'stop' an S3 bucket. Use 'delete' instead.")
        else:
            delete_s3(args.resource_id)

    elif args.resource_type == 'lambda':
        if args.action == 'create':
            lambda_name = create_lambda()
            if lambda_name:
                update_state('lambda_function_name', lambda_name)
                print(f"-> Saved Name {lambda_name} to state.json")
        elif args.action == 'stop':
            print("Error: You cannot 'stop' a Lambda function. Use 'delete' instead.")
        else:
            delete_lambda(args.resource_id)

    print("\n=======================================")
    print("   Operation Complete!")
    print("=======================================")

if __name__ == "__main__":
    main()
