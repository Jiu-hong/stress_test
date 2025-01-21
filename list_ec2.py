import boto3
import os


def list_running_ec2():
    ec2_list = {}
    ec2_client = boto3.client("ec2", region_name="us-west-2",
                              aws_access_key_id=os.getenv(
                                  "AWS_ACCESS_KEY_ID"),
                              aws_secret_access_key=os.getenv(
                                  "AWS_SECRET_ACCESS_KEY"),
                              aws_session_token=os.getenv("AWS_SESSION_TOKEN"))

    # filter only tag with ChainName: casper-test-jh
    custom_filter = [{
        'Name': 'tag:ChainName',
        'Values': ['casper-test-jh']}]

    # return all instances
    response = ec2_client.describe_instances(
        Filters=custom_filter)
    instances_list = response["Reservations"]

    # extract instance name and public ip
    for member in instances_list:
        if member["Instances"][0]["State"]["Name"] == "running":
            public_ip = member["Instances"][0]["PublicIpAddress"]
            for tags in member["Instances"][0]["Tags"]:
                if tags["Key"] == "Name":
                    # exclude stest-test-jh-0
                    if tags["Value"] != "casper-stest-test-jh-0":
                        instance_name = tags["Value"]
                        ec2_list[instance_name] = public_ip

    return ec2_list
