#!/bin/bash
# ==============================================================================
# Cloud Automation Scheduler Script (Bash/Cron)
# This script is designed to be run via a Cron Job to automatically trigger
# the AWS provisioning lifecycle.
#
# To schedule this to run daily at 8:00 AM, add the following to crontab -e:
# 0 8 * * * /path/to/cloud-automation-project/scripts/schedule_automation.sh
# ==============================================================================

# Get the absolute directory of the project
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "======================================="
echo " Starting Scheduled AWS Automation"
echo " Time: $(date)"
echo "======================================="

# Navigate to project directory
cd "$PROJECT_DIR" || exit

# Run the provisioning and teardown lifecycle
python provision_all.py

echo "======================================="
echo " Scheduled Automation Completed"
echo " Time: $(date)"
echo "======================================="
