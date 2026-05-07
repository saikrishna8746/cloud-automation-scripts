import boto3
import sys

def setup_sns_topic(email_address: str):
    """
    Creates an SNS topic for admin alerts and subscribes the given email address.
    """
    sns = boto3.client('sns')
    topic_name = "Admin-Alerts"
    
    try:
        # Create topic (is idempotent, so running it again just returns the ARN)
        print(f"Creating/retrieving SNS Topic: {topic_name}...")
        response = sns.create_topic(Name=topic_name)
        topic_arn = response['TopicArn']
        print(f"Success! Topic ARN: {topic_arn}")
        
        # Subscribe email
        print(f"Subscribing {email_address} to topic...")
        sns.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_address
        )
        print("\n--- IMPORTANT ---")
        print(f"1. Check the inbox for '{email_address}'. You will receive a 'AWS Notification - Subscription Confirmation' email.")
        print("2. Click the 'Confirm subscription' link in that email.")
        print("3. Copy the Topic ARN below and add it to your .env file as SNS_TOPIC_ARN:")
        print(f"\nSNS_TOPIC_ARN={topic_arn}")
        
    except Exception as e:
        print(f"Error setting up SNS: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup_notifications.py <admin_email_address>")
        sys.exit(1)
        
    admin_email = sys.argv[1]
    setup_sns_topic(admin_email)
