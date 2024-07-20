# EC2 Rescue Script

## Overview

This script automates the process of running AWS remediation on Windows Server EC2 instances using the `AWSSupport-StartEC2RescueWorkflow` Systems Manager automation runbook. Addtionally, it provides a report file containing the execution IDs which can be used to verify the status of the jobs. See https://repost.aws/en/knowledge-center/ec2-instance-crowdstrike-agent for more details.

## Features

- Starts the EC2 Rescue workflow on specified instances.
- Provides a detailed report with execution IDs.
- Allows reviewing the status of previous rescue operations.

## Prerequisites

- Python 3.x
- Boto3

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/m-quintero/ec2_rescue.git
    cd ec2_rescue
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Start EC2 Rescue

1. Create a file containing the instance IDs (one per line).
2. Run the script and choose option `1`.
3. Enter the filename containing the instance IDs and the AWS region.

    ```sh
    python ec2_rescue.py
    ```

### Review Status

1. Ensure you have the report file generated from the previous step.
2. Run the script and choose option `2`.
3. Enter the report filename and the AWS region.

    ```sh
    python ec2_rescue.py
    ```

## Example

### Starting EC2 Rescue

1. Create a file `instances.txt` with the following content:
    ```
    i-0abcd1234efgh5678
    i-0abcd1234efgh5679
    ```

2. Run the script:
    ```sh
    python ec2_rescue.py
    ```

3. Choose option `1` and enter the filename and AWS region:
    ```
    Choose an option:
    1. Start EC2 Rescue
    2. Review Status
    Enter 1 or 2: 1
    Enter the file name containing Instance IDs: instances.txt
    Enter the AWS Region: us-east-1
    ```

### Reviewing Status

1. Ensure you have the report file generated from the previous step (e.g., `BATCH_20230720_123456.txt`).

2. Run the script:
    ```sh
    python ec2_rescue.py
    ```

3. Choose option `2` and enter the report filename and AWS region:
    ```
    Choose an option:
    1. Start EC2 Rescue
    2. Review Status
    Enter 1 or 2: 2
    Enter the report file name: BATCH_20230720_123456.txt
    Enter the AWS Region: us-east-1
    ```

## License

Not yet determined

## Author

Michael Quintero (michael.quintero@rackspace.com or michael.quintero@gmail.com)
