module "detect_unused_eips" {
  source           = "git@github.com:cloudmitigator/reflex.git//modules/cwe_lambda?ref=v0.0.1"
  rule_name        = "DetectUnusedEIPs"
  rule_description = "Rule to detect Unused Elastic IP Addresses"

  event_pattern = <<PATTERN
{
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "source": [
    "aws.ec2"
  ],
  "detail": {
    "eventSource": [
      "ec2.amazonaws.com"
    ],
    "eventName": [
      "DisassociateAddress"
    ]
  }
}
PATTERN

  function_name            = "DetectUnusedEIPs"
  source_code_dir          = "${path.module}/source"
  handler                  = "detect_unused_eips.lambda_handler"
  lambda_runtime           = "python3.7"
  environment_variable_map = { SNS_TOPIC = module.detect_unused_eips.sns_topic_arn }
  custom_lambda_policy     = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:DescribeAddresses"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF



  queue_name    = "DetectUnusedEIPs"
  delay_seconds = 900

  target_id = "DetectUnusedEIPs"

  topic_name = "DetectUnusedEIPs"
  email      = var.email
}
