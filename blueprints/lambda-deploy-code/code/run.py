import boto3

# This script makes a lot of assumptions and is only a proof of concept.
# It looks for a container tagged with dev and adds a live tag.
# credit to https://aws.amazon.com/blogs/compute/amazon-ecs-at-the-climate-corporation-using-ecr-and-multiple-accounts-for-isolated-regression-testing/ for the idea

client = boto3.client('ecr')

registry_id = '346135719058'
registry_name = 'demo-app'

handler(event, context):
    # Gets the container with the tag dev
    response = client.batch_get_image(
        registryId=registry_id,
        repositoryName=registry_name,
        imageIds=[
            {
                'imageTag': 'dev'
            }
        ]
    )

    # Filers out all but the manifest
    dev_manifest = response['images'][0]['imageManifest']

    # pushes the old manifest with an additional tag of live
    change_tag = client.put_image(
        registryId=registry_id,
        repositoryName=registry_name,
        imageManifest=dev_manifest,
        imageTag='live'
    )
