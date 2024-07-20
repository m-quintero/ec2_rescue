"""
Script Name: ec2_rescue.py
Author: michael.quintero@rackspace.com
Description: This script runs aws remediation on Windows Server ec2 instances, provides a report file which contains the execution ids & can be used when running step 2 to verify the status of the jobs. USE AT YOUR OWN RISK!
More info: This script is built around the AWSSupport-StartEC2RescueWorkflow Systems Manager automation runbook solution provided by AWS, see here - https://repost.aws/en/knowledge-center/ec2-instance-crowdstrike-agent
Usage: python3 ec2_rescue.py, answer the questions, bam! Accepts a file which contains the ec2 ids, NOT TAG NAMES!!! Ensure that all instances in the file being referenced are in the same region. Assumes your creds are properly set for the account.
Pre-Requisites: Python3 & Boto3
"""

import boto3
import json
import time
from datetime import datetime

# Using the AWS provided, automation runbook
def start_ec2_rescue(instance_id, region, report_file):
    ssm_client = boto3.client('ssm', region_name=region)

    response = ssm_client.start_automation_execution(
        DocumentName='AWSSupport-StartEC2RescueWorkflow',
        DocumentVersion='$DEFAULT',
        Parameters={
            'InstanceId': [instance_id],
            'OfflineScript': ['Z2V0LWNoaWxkaXRlbSAtcGF0aCAiJGVudjpFQzJSRVNDVUVfT0ZGTElORV9EUklWRVxXaW5kb3dzXFN5c3RlbTMyXGRyaXZlcnNcQ3Jvd2RTdHJpa2VcIiAtSW5jbHVkZSBDLTAwMDAwMjkxKi5zeXMgLVJlY3Vyc2UgfCBmb3JlYWNoIHsgJF8uRGVsZXRlKCl9'],
            'EC2RescueInstanceType': ['t3.medium'],
            'SubnetId': ['SelectedInstanceSubnet'],
            'S3Prefix': ['AWSSupport-EC2Rescue'],
            'AMIPrefix': ['AWSSupport-EC2Rescue'],
            'CreatePreEC2RescueBackup': ['False'],
            'CreatePostEC2RescueBackup': ['False'],
            'UniqueId': ['{{ automation:EXECUTION_ID }}'],
            'AllowEncryptedVolume': ['True'],
            'AssociatePublicIpAddress': ['False']
        }
    )

    execution_id = response['AutomationExecutionId']
    print(f'Started Automation Execution for Instance {instance_id} with ID: {execution_id}')

    # Save execution ID to report file which is to be used with the 2nd option, job status
    with open(report_file, 'a') as file:
        file.write(f'{datetime.now()} - {instance_id} - {execution_id}\n')

    return execution_id

def get_automation_execution_status(execution_id, region):
    ssm_client = boto3.client('ssm', region_name=region)

    response = ssm_client.get_automation_execution(
        AutomationExecutionId=execution_id
    )

    status = response['AutomationExecution']['AutomationExecutionStatus']
    instance_id = response['AutomationExecution']['Parameters']['InstanceId'][0]
    print(f'Execution ID: {execution_id}, Instance ID: {instance_id}, Status: {status}')

    return {
        'ExecutionId': execution_id,
        'InstanceId': instance_id,
        'Status': status
    }

# I ensured that the report uses a friendly naming convention
def generate_report_file():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f'BATCH_{current_time}.txt'
    return report_file

def main():
    option = input("Choose an option:\n1. Start EC2 Rescue\n2. Review Status\nEnter 1 or 2: ")

    if option == '1':
        instance_file = input('Enter the file name containing Instance IDs: ')
        region = input('Enter the AWS Region: ')
        report_file = generate_report_file()

        try:
            with open(instance_file, 'r') as file:
                for line in file:
                    instance_id = line.strip()
                    if instance_id:
                        start_ec2_rescue(instance_id, region, report_file)
            print(f'Automation executions started. Report saved in {report_file}')
        except FileNotFoundError:
            print(f"Instance file {instance_file} not found.")

    elif option == '2':
        report_file = input('Enter the report file name: ')
        region = input('Enter the AWS Region: ')

        try:
            with open(report_file, 'r') as file:
                for line in file:
                    _, instance_id, execution_id = line.strip().split(' - ')
                    details = get_automation_execution_status(execution_id, region)
                    print(json.dumps(details, indent=4, default=str))
        except FileNotFoundError:
            print(f"Report file {report_file} not found.")
    else:
        print("Invalid option. Please enter 1 or 2.")

if __name__ == '__main__':
    main()
