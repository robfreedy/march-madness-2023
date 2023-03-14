# March Madness 2023 Predictions powered by Prefect
 This is a repo to store Prefect flow code for March Madness 2023 predictions

 **Note: This README provides a tutorial for Prefect + AWS EKS. You can use any other Prefect Storage and Infrastructure Blocks to run this flow.** 

## Initial Requiments
- Prefect Cloud Account and Workspace (see [here](https://docs.prefect.io/) to get started with Prefect)
- Rapid API account and key (see [here](https://rapidapi.com/hub) to create an account and API Key)
- AWS account as well as IAM permissions for S3, ECR, and EKS

## Setting up the Infrastructure

### EKS Cluster

This workload does not require a complicated setup, so I decided to use eksctl to create the cluster in AWS.

Instructions for downloading eksctl can be found [here](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)

Instructions for setting up an EKS Cluster using eksctl can be found [here](https://discourse.prefect.io/t/how-to-create-a-kubernetes-cluster-on-aws-eks/1041)

To scale up nodes for the agent to run on, run the following command
```
eksctl scale nodegroup --cluster=<cluster_name> --nodes=<num_nodes> --name=<node_group_name>
```

### Deploying the Agent
The agent was deployed using the following [Discourse article](https://discourse.prefect.io/t/deploying-prefect-agents-on-kubernetes/1298) as a guide.

Kubernetes secrets were created for the PREFECT_API_URL and the PREFECT_API_KEY (see third section of the above discourse post).

The work-queue name in the agent start command also got replaced by march-madness.

### Docker Image

The following documentation can be used to create the Docker image and push it to ECR. This repository is used in the Prefect KubernetesJob block (see docs [here](https://aws.plainenglish.io/how-to-push-an-image-to-aws-ecr-b2be848c2ef)).

The image is based off of the Dockerfile in this repository and is used in the KubernetesJob block below.

Note: For those building the image on Macs, you may need to build the image with this flag: 
```
--platform=linux/amd64
```

### Storage - S3

An S3 bucket was created in the same account as the above ECR image. 

Then, an S3 block was created in the Prefect Cloud UI and referenced in the deployment command below. 

For more information on flow storage, see the Prefect Docs [here](https://docs.prefect.io/concepts/storage/).

### Execution Environment - KubernetesJob

A Kubernetes Job block was created with the details from the eksctl cluster that was created above as well as the image that was created and pushed to the ECR repository.

To see more information about Prefect infrastrucute blocks, see the Prefect Docs [here](https://docs.prefect.io/concepts/infrastructure/).

I set the Finished Job TTL to 30000 for Kubernetes Job cleanup, but if you would like to retain the jobs in the cluster you can leave this field blank. 

Also, make sure to include the s3fs module in the environment section of this block in order to pull the flow from the S3 bucket storage block. 

```
{
  "EXTRA_PIP_PACKAGES": "s3fs"
}
```

### Deployment commands

In order to run this Prefect flow in the environment defined above, we need to build and apply a deployment in a Prefect Workspace. 
For more information on deployments, see the Prefect Docs [here](https://docs.prefect.io/concepts/deployments/)

Prefect deployment build command:
```
prefect deployment build flow.py:main -n march-madness-2023 -q march-madness -ib kubernetes-job/march-madness -sb s3/march-madness
```

Prefect deployment apply command:
```
prefect deployment apply main-deployment.yaml
```

After these commands are run, the flow code should be uploaded to the S3 bucket as storage and the deployment should appear in the Prefect UI. 

### Basketball API and Secret

The details of the Basketball API can be found [here](https://rapidapi.com/api-sports/api/api-basketball/details)

A Prefect secret block was created to store and access the API Key. For more information on the secret block, see the documentation [here](https://docs.prefect.io/api-ref/prefect/blocks/system/#prefect.blocks.system.Secret)

## What does this flow do?

This flow takes in data from the free Basketball API and predicts the result of the first games that each team in the NCAA tournament plays. From there, the winners are ranked based on a calculated score. This score is a combination of average points scored per game, average points allowed per game, and winning percentage. Improvements to this algorithm will be made to better predict next years tournament. 



## File Reference
- flow.py - main flow script that provides March Madness Predictions
- teams.json - json file that stores the RapidAPI id of each of the teams in the NCAA tournament as well as the id of their initial opponent
- Dockerfile - builds the image that is upload to ECR and used in the KubernetesJob block
- requirements.txt - dependencies for flow.py that are baked into the Docker image
- agent.yaml - the agent yaml file that contains all the config to run an agent in a Kubernetes cluster
- .prefectignore - this file is used to specify files that do not get uploaded to S3 storages



