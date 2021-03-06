# AWS Docker Build Pipeline
An example CloudFormation implementation of a multi-environment, serverless CI environment using CodePipeline, CodeBuild and CodeCommit deploying to ElasticBeanstalk.

![diagram](https://raw.githubusercontent.com/francis-io/aws-docker-build-pipeline/master/images/diagram.png)

# TODO
- [x] Code repo and Elastic Container Registry per environment.
- [x] CodeBuild setup, pushing to ECR.
- [x] CodePipeline sourcing the code repo and running CodeBuild.
- [ ] Working docker ElasticBeanstalk environment.
- [x] Finalize method to migrate containers between environments.
- [ ] Write and deploy env migration lambda using tags.
- [ ] Blue/Green deployments and rollback plan.
- [x] Commit example Code and build config. Added to example-code dir.

# Requirements
* php (I installed php 5.6, needed for composer and stackformation)
* composer
* [StackFormation](https://stackformation.readthedocs.io/en/latest/GettingStarted/index.html)

# Setup
Install StackFormation dependencies:
(https://stackformation.readthedocs.io/en/latest/)

Run: `./bin/composer install`

(On my Fedora 24 machine I also had to install php-xml, jq and make sure date.timezone was populated in /etc/php.ini)

* Run `vendor/bin/stackformation.php setup` and populate with AMI keys with enough permissions to create CloudFormation stacks.

Setup the service role mentioned below in "Manual Service Role Setup".

# Stack Setup

Each CloudFormation stack can be created by calling the stack name usingthe following command:

```vendor/bin/stackformation.php blueprint:deploy '{var:ProjectName}-repository'```

After creating the Codecommit stack, you need to initialise the repository manually and create a branch. I pushed to master manually.

## TODO complete documentation.

## Manual Service Role Setup
You need to manually create a service role for CloudFormation to assume. I can't find any way to automate this. The permissions may be a little wide, you might want to tone them back if you intend to use this beyond a testing environment.

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
        },
        {
            "Sid": "CodecommitGet",
            "Effect": "Allow",
            "Action": [
                "codecommit:GetBranch",
                "codecommit:GetCommit",
                "codecommit:UploadArchive",
                "codecommit:GetUploadArchiveStatus",
                "codecommit:CancelUploadArchive",
                "codebuild:*"
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

## Adding tags to ECR images
MANIFEST=$(aws ecr batch-get-image --repository-name wip-docker --image-ids imageTag=latest --query images[].imageManifest --output text)
TAG=demo
aws ecr put-image --repository-name wip-docker --image-tag $TAG --image-manifest "$MANIFEST" 
