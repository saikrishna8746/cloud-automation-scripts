import argparse
import sys
import os

# Add scripts directory to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from delete_ec2 import delete_instance, stop_instance
from delete_s3_bucket import delete_s3
from delete_lambda import delete_lambda

def main():
    parser = argparse.ArgumentParser(description="Cloud Automation CLI Manager")
    parser.add_argument('action', choices=['stop', 'terminate', 'delete'], help="Action to perform")
    parser.add_argument('resource_type', choices=['ec2', 's3', 'lambda'], help="Type of resource")
    parser.add_argument('resource_id', help="The ID or Name of the specific resource")

    args = parser.parse_args()

    print("=======================================")
    print(f"   Executing: {args.action.upper()} on {args.resource_type.upper()} ({args.resource_id})")
    print("=======================================\n")

    if args.resource_type == 'ec2':
        if args.action == 'stop':
            stop_instance(args.resource_id)
        elif args.action in ['terminate', 'delete']:
            delete_instance(args.resource_id)

    elif args.resource_type == 's3':
        if args.action == 'stop':
            print("Error: You cannot 'stop' an S3 bucket. Use 'delete' instead.")
        else:
            delete_s3(args.resource_id)

    elif args.resource_type == 'lambda':
        if args.action == 'stop':
            print("Error: You cannot 'stop' a Lambda function. Use 'delete' instead.")
        else:
            delete_lambda(args.resource_id)

    print("\n=======================================")
    print("   Operation Complete!")
    print("=======================================")

if __name__ == "__main__":
    main()
