<#
.SYNOPSIS
    Cloud Automation Scheduler Script (PowerShell)
    
.DESCRIPTION
    This script is designed to be run via Windows Task Scheduler to automatically 
    trigger the AWS provisioning lifecycle.

.EXAMPLE
    To schedule this via Task Scheduler:
    1. Open Task Scheduler -> Create Basic Task
    2. Trigger: Daily at 8:00 AM
    3. Action: Start a program
    4. Program/script: powershell.exe
    5. Add arguments: -ExecutionPolicy Bypass -File "C:\path\to\cloud-automation-project\scripts\schedule_automation.ps1"
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host " Starting Scheduled AWS Automation" -ForegroundColor Cyan
Write-Host " Time: $(Get-Date)" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Navigate to project directory
Set-Location -Path $ProjectDir

# Run the provisioning and teardown lifecycle
python provision_all.py

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host " Scheduled Automation Completed" -ForegroundColor Cyan
Write-Host " Time: $(Get-Date)" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
