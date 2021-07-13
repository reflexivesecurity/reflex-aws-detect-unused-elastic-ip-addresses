""" Module for enforcing S3EncryptionRule """

import json
import os

import boto3
from reflex_core import AWSRule, subscription_confirmation


class UnusedEIPRule(AWSRule):
    """ AWS rule for detecting unused EIPs. """

    client = boto3.client("ec2")

    def __init__(self, event):
        super().__init__(event)
        self.unattached_eips = []

    def extract_event_data(self, event):
        """ To be implemented by every rule """
        self.raw_event = event

    def resource_compliant(self):
        return not self.any_detached_eips()

    def any_detached_eips(self):
        """ Returns True if the bucket is encrypted, False otherwise """
        all_addresses = self.client.describe_addresses()["Addresses"]
        for address in all_addresses:
            if "AssociationId" not in address.keys():
                self.unattached_eips.append(address["AllocationId"])
        if self.unattached_eips:
            return True
        return False

    def get_remediation_message(self):
        """ Returns a message about the remediation action that occurred """
        return f"The following unattached EIPs exist an hour after a disassociate ip: {self.unattached_eips}"


def lambda_handler(event, _):
    """ Handles the incoming event """
    print(event)
    event_payload = json.loads(event["Records"][0]["body"])
    if subscription_confirmation.is_subscription_confirmation(event_payload):
        subscription_confirmation.confirm_subscription(event_payload)
        return
    unused_eip_rule = UnusedEIPRule(event_payload)
    unused_eip_rule.run_compliance_rule()
