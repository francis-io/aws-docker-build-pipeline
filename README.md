# AWS Docker Build Pipeline
An example CloudFormation implementation of a multi-environment, serverless CI environment using CodePipeline, CodeBuild and CodeCommit.

#Requirements
* php (I installed php 5.6, needed for composer and stackformation)
* composer
* [StackFormation](https://stackformation.readthedocs.io/en/latest/GettingStarted/index.html)

# Setup
Install StackFormation dependencies:
(https://stackformation.readthedocs.io/en/latest/)

Run: `./bin/composer install`

(On my Fedora 24 machine I also had to install php-xml, jq and make sure date.timezone was populated in /etc/php.ini)

* Run `vendor/bin/stackformation.php setup` and populate with AMI keys with enough permissions to create CloudFormation stacks.

# Repository Setup
You need to create an environment specific repository:

`export Environment=live && vendor/bin/stackformation.php blueprint:deploy '{env:Environment}-{var:ProjectName}-repository'`

After creating the Codecommit stack, you need to initialise the repository manually and create a branch. I pushed to master manually.

# CodeBuild Setup
You need to manually create a service role for CloudFormation to assume. I can't find any way to automate this.

Login to an AWS root/Administrator account. Navigate to IAM, Policies, Create Your Own Policy. 

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudWatchLogsPolicy",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Sid": "CodeCommitPolicy",
      "Effect": "Allow",
      "Action": [
        "codecommit:GitPull"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Sid": "S3GetObjectPolicy",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Sid": "S3PutObjectPolicy",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```


Create a Role, Create New Role. Select "AWS Service Role" Amazon EC2. Search and select the previously created Service Policy. Once created, edit the role, Trust Relationship. Change the service from "ec2.amazonaws.com" to "codebuild.amazonaws.com". Note the ARN for this role in the global blueprints.yml file.

The policy name can be added to the root blueprint.yml file.
