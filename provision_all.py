import sys
import os
import time
import datetime
import argparse

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

    wait_teardown = settings.WAIT_TIME_SECONDS
    while wait_teardown > 0:
        sys.stdout.write(f"\rWaiting {wait_teardown} seconds before automatic teardown...   ")
        sys.stdout.flush()
        time.sleep(1)
        wait_teardown -= 1
    print("\n")

    # Automatically call the destroy script
    destroy_all.main()

def wait_for_time(target_time_str):
    """Parses a time string and pauses execution until that time is reached."""
    target_time_str = target_time_str.replace(" ", "").upper()
    try:
        # Try 24-hour format
        target_time = datetime.datetime.strptime(target_time_str, "%H:%M").time()
    except ValueError:
        try:
            # Try 12-hour format
            target_time = datetime.datetime.strptime(target_time_str, "%I:%M%p").time()
        except ValueError:
            print("Error: Invalid time format. Please use '15:10' or '3:10PM'.")
            sys.exit(1)
            
    now = datetime.datetime.now()
    target_datetime = datetime.datetime.combine(now.date(), target_time)
    
    # If the target time has already passed today, schedule for tomorrow
    if target_datetime <= now:
        target_datetime += datetime.timedelta(days=1)
        
    wait_seconds = int((target_datetime - now).total_seconds())
    
    print(f"=======================================")
    print(f" Scheduled to run at: {target_datetime.strftime('%I:%M %p on %Y-%m-%d')}")
    print(f"=======================================\n")
    
    while wait_seconds > 0:
        mins, secs = divmod(wait_seconds, 60)
        hours, mins = divmod(mins, 60)
        time_format = f"{hours:02d}:{mins:02d}:{secs:02d}"
        
        sys.stdout.write(f"\rWaiting for {time_format} until execution...")
        sys.stdout.flush()
        time.sleep(1)
        wait_seconds -= 1
        
    print("\n\nTime reached! Starting automation...\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provision Cloud Resources")
    parser.add_argument('--time', type=str, help="Specific time to run the script (e.g., '15:10' or '3:10PM')")
    args = parser.parse_args()

    if args.time:
        wait_for_time(args.time)

    main()
