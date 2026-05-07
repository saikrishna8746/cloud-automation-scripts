# Cloud Automation Scripting Project

This project provides a suite of automated Python scripts to provision, manage, and tear down AWS infrastructure (EC2, S3, and Lambda). It is designed to demonstrate Infrastructure as Code (IaC) principles using the AWS SDK for Python (`boto3`), complete with centralized configuration, robust logging, and real-time email notifications.

## 🚀 Features
- **EC2 Management:** Automated provisioning and termination of EC2 instances with randomized naming.
- **S3 Management:** Creation and cleanup of S3 buckets.
- **Serverless (Lambda):** Automated deployment of Lambda functions from local `.zip` packages.
- **Event-Driven Notifications:** Real-time email alerts sent to an administrator via Amazon SNS whenever resources are created or destroyed.
- **Centralized Configuration:** Easily manage AWS Regions, AMIs, Instance Types, and IAM Roles from a single `settings.py` file.
- **State Management:** A custom `state.json` tracks provisioned resources so you can tear down your entire infrastructure cleanly with a single command.
- **Error Handling & Logging:** All actions are safely wrapped in `try/except` blocks and logged to `logs/automation.log`.

---

## 📂 Project Structure

```text
cloud-automation-project/
├── .env.example          # Template for environment variables (SNS Topic ARN, etc.)
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── bash/                 # Directory for bash/powershell scripts
├── config/               # Project configuration files (YAML)
├── docs/                 # Additional usage documentation
├── lambda/               # Lambda function source code and .zip packages
├── logs/                 # Automation logs (automation.log)
├── provision_all.py      # Master script to provision all infrastructure
├── destroy_all.py        # Master script to tear down all infrastructure
├── manage.py             # Unified CLI to stop/terminate specific resources
├── scripts/              # Main Python automation scripts
│   ├── settings.py       # Centralized AWS configuration (Region, AMIs, Roles)
│   ├── state_utils.py    # Helper module for reading/writing state.json
│   ├── sns_utils.py      # Helper module for sending Amazon SNS emails
│   ├── setup_notifications.py # Script to initialize the SNS topic
│   ├── create_ec2.py     # Provisions an EC2 instance
│   ├── delete_ec2.py     # Terminates an EC2 instance
│   ├── create_s3_bucket.py # Provisions an S3 bucket
│   ├── delete_s3_bucket.py # Deletes a provisioned S3 bucket
│   ├── create_lambda.py  # Deploys a Lambda function
│   └── delete_lambda.py  # Deletes a Lambda function
└── tests/                # Automated testing suite
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.9+
- AWS CLI installed and configured with appropriate IAM permissions (`aws configure`)
- Git

### 2. Install Dependencies
Install the required Python packages (such as `boto3` and `python-dotenv`):
```bash
pip install -r requirements.txt
# Alternatively:
pip install boto3 python-dotenv
```

### 3. Configure AWS Settings
Open `scripts/settings.py` and ensure the values match your AWS environment:
```python
AWS_REGION = 'ap-south-1'
EC2_AMI_ID = 'ami-034a8236c75419857'
EC2_INSTANCE_TYPE = 't3.micro'
LAMBDA_EXECUTION_ROLE_ARN = 'arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role'
```

### 4. Enable Email Notifications
To receive email alerts when infrastructure changes occur:
1. Run the setup script with your email address:
   ```bash
   python scripts/setup_notifications.py your-email@example.com
   ```
2. Check your email inbox and click **"Confirm subscription"**.
3. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Paste the `SNS_TOPIC_ARN` outputted by the setup script into your `.env` file.

---

## 💻 Usage

Navigate to the project root directory and run the scripts using Python. 

### Provision Everything
Launch an EC2 instance, S3 bucket, and Lambda function with a single command. The resource IDs will be saved to `state.json`.
```bash
python provision_all.py
```

### Destroy Everything
Read `state.json` and cleanly tear down all infrastructure that was provisioned.
```bash
python destroy_all.py
```

### Unified CLI Tool
You can manage specific resources individually using the unified CLI:
```bash
# Create individual resources (automatically saves to state.json)
python manage.py create ec2
python manage.py create s3
python manage.py create lambda

# Stop an EC2 Instance (Pause it without destroying)
python manage.py stop ec2 i-0123456789abcdef0

# Terminate an EC2 Instance (Destroy it)
python manage.py terminate ec2 i-0123456789abcdef0

# Delete an S3 Bucket
python manage.py delete s3 your-bucket-name

# Delete a Lambda Function
python manage.py delete lambda your-function-name
```

### Run Individual Scripts
You can also run the modular scripts individually:
```bash
# EC2
python scripts/create_ec2.py
python scripts/delete_ec2.py i-0123456789abcdef0

# S3
python scripts/create_s3_bucket.py
python scripts/delete_s3_bucket.py your-bucket-name

# Lambda
python scripts/create_lambda.py
python scripts/delete_lambda.py your-function-name
```

---

## 📝 Logging
All infrastructure actions (successes and errors) are logged automatically. You can review the execution history at any time by opening:
`logs/automation.log`

## 🛡️ License
This project is created for educational purposes as part of Project 6 — Cloud Automation Scripting Focus.
