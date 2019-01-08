# Overview

Simple DNS server to provide AWS name resolution based on instance name. It is a fork of the original https://github.com/samuelcolvin/dnserver, which is a standard DNS server sans the AWS. This service is intended to be behind a robust caching DNS server such as bind or unbound, with stub zones configured. The caching DNS server should be configured to forward all requests to the AWS internal DNS service with the excpeption of the following zones which should be forwarded to this python service.

us-east-1.<custom>
us-east-2.<custom>
...

There should be a zone for each AWS region. The domain name should be <region-name>.<custom>. The ending custom part is optional and you can choose to mirror the aws internal domain name or use your own. For example...

us-east-1.compute.internal

The default region is us-east-1. If a request comes in with only the hostname, us-east-1 will be used. You must install and configure boto3.

# AWS Configuration
You will need to create a policy and user
1. Go to IAM > Policies
2. Create Policy
3. Select JSON tab and paste the following in, overwritting the existing value
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeHosts",
                "ec2:DescribeAddresses",
                "ec2:DescribeInstances",
                "ec2:DescribeNetworkInterfaceAttribute",
                "ec2:DescribeInstanceAttribute",
                "ec2:DescribeInstanceStatus"
            ],
            "Resource": "*"
        }
    ]
}
4. Review Policy, Provide a name such as EC2_LIST_METADATA
5. Create Policy

Next Create a User
1. Got to IAM > Users
2. Add User
3. Give it a name and select Programmatic Access
4. Click Next to go to permissions
5. Select Attach Existing Policy
6. Search for the policy you just created by name, then check the box next to it
7. Click next until you get to the last step
8. Be sure to copy the Access Key ID and the Secret Access Key and save in a safe place. You will not be able to get the key value from AWS later.

# Installation
These instructions are for development and testing purposes. Production should be containerized, this is still being developed.
The following assumes a fresh ubuntu 16.04 LTS VM using the AWS AMI.
      
      sudo apt-get update
      sudo apt-get install python3-pip
      cd /src-directory
      sudo pip3 isntall -r requirements.txt
      sudo mkdir /zones
      sudo cp example_zones.txt /zones/zones.txt
      mkdir ~/.aws

Create ~/.aws/credentials with the following content. Replace the access key ID and secret access key values with your values you saved from the AWS Configuration steps above
      
      [default]
      aws_access_key_id=AKIAABC123
      aws_secret_access_key=1234abcdf

CREATE ~/.aws/config with the following content. Replace the region with your desired default region

      [default]
      region=us-east-1

# Start the Service
sudo python3 dnserver.py





