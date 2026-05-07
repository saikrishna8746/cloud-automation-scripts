import boto3
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

def send_admin_alert(subject: str, message: str) -> None:
    """
    Sends an email alert to the admin via Amazon SNS.
    """
    if not SNS_TOPIC_ARN:
        logging.warning("SNS_TOPIC_ARN not found in environment. Skipping email alert.")
        return

    try:
        sns = boto3.client('sns')
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject[:100],  # SNS Subject max length is 100 chars
            Message=message
        )
        logging.info(f"Successfully sent admin alert: {subject} (MessageId: {response.get('MessageId')})")
    except Exception as e:
        logging.error(f"Failed to send admin alert '{subject}': {e}")
