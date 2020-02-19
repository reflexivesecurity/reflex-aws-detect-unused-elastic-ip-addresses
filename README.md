# reflex-aws-detect-unused-elastic-ip-addresses
A Reflex rule for detecting unused elastic IP addresses.

## Usage
To use this rule either add it to your `reflex.yaml` configuration file:  
```
version: 0.1

providers:
  - aws

measures:
  - reflex-aws-detect-unused-elastic-ip-addresses:
      email: "example@example.com"
```

or add it directly to your Terraform:  
```
...

module "reflex-aws-detect-unused-elastic-ip-addresses" {
  source           = "github.com/cloudmitigator/reflex-aws-detect-unused-elastic-ip-addresses"
  email            = "example@example.com"
}

...
```

## License
This Reflex rule is made available under the MPL 2.0 license. For more information view the [LICENSE](https://github.com/cloudmitigator/reflex-aws-detect-unused-elastic-ip-addresses/blob/master/LICENSE) 
