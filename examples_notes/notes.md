# CloudFormation

## Resources
- [AWS CloudFormation Resource Type Templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)

## Parameters
- [AWS CloudFormation Paramters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html)
- [AWS CloudFormation Reference Function](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)
### Syntax
#### Declare Paramters
```yaml
Parameters:
  InstanceTypeParameter:
    Type: String
    Default: t2.micro
    AllowedValues:
      - t2.micro
      - m1.small
      - m1.large
    Description: Enter t2.micro, m1.small, or m1.large. Default is t2.micro.
```
#### Reference
```yaml
Ec2Instance1:
  Type: AWS::EC2::Instance
  Properties:
    InstanceType:
      Ref: InstanceTypeParameter
    ImageId: ami-0ff8a91507f77f867

Ec2Instance2:
  Type: AWS::EC2::Instance
  Properties:
    InstanceType: !Ref InstanceTypeParameter
    ImageId: ami-0ff8a91507f77f867
```

## Mappings
- [AWS CloudFormation Mappings](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html)
### Syntax
#### Declaration
```yaml
Mappings: 
  RegionMap: 
      us-east-1: 
        32: "ami-6411e20d"
        64: "ami-7a11e213"
      us-west-1: 
        32: "ami-c9c7978c"
        64: "ami-cfc7978a"
```
#### Reference
```yaml
Resources: 
  myEC2Instance: 
    Type: "AWS::EC2::Instance"
    Properties: 
      # ImageId: !FindInMap [ RegionMap, !Ref "us-east-1", 32 ]
      ImageId: !FindInMap [ RegionMap, !Ref "AWS::Region", 32 ]
      InstanceType: m1.small
  TestInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !FindInMap
        - !Ref 'AWS::Region'
        - 64
      InstanceType: m1.small
```

## Outputs
**CloudFormation doesn't redact or obfuscate any information you include in the Outputs section. We strongly recommend you don't use this section to output sensitive information, such as passwords or secrets.**
### Syntax
#### Simple Stack
```yaml
Outputs:
  BackupLoadBalancerDNSName:
    Description: The DNSName of the backup load balancer
    Value: !GetAtt BackupLoadBalancer.DNSName
    Condition: CreateProdResources
  InstanceID:
    Description: The Instance ID
    Value: !Ref EC2Instance
```
#### Cross Stack
```yaml
Outputs:
  StackVPC:
    Description: The ID of the VPC
    Value: !Ref MyVPC
    Export:
      Name: !Sub "${AWS::StackName}-VPCID"
```

## Intrinsic Functions
- [Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)
- Includes:
  - Fn::Base64
  - Fn::Cidr
  - Condition functions
  - Fn::FindInMap
  - Fn::GetAtt
  - Fn::GetAZs
  - Fn::ImportValue
  - Fn::Join
  - Fn::Length
  - Fn::Select
  - Fn::Split
  - Fn::Sub
  - Fn::ToJsonString
  - Fn::Transform
  - Ref

## Nested Stack
- [AWS::CloudFormation::Stack](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html)
- On deletion, parent stack might remain in delete_failed state. To fix:
  - reselect parent stack
  - reselect delete
  - popup screen will ask which children stacks to keep:
    - select children stacks causing dependency issue
  - proceed to delete parent stack
  - proceed to individually delete children stacks