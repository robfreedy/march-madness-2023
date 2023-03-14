# March Madness 2023 Predictions powered by Prefect
 This is a repo to store Prefect flow code for March Madness 2023 predictions

 **Note: This README provides a tutorial for Prefect + AWS EKS. You can use any other Prefect Storage and Infrastructure Blocks to run this flow** 

## Initial Requiments
- Prefect Cloud Account and workspace
- Rapid API account and key
- AWS account

## Setting up the Infrastructure

### EKS Cluster

This workload does not require a complicated setup, so I decided to use eksctl to create the cluster in AWS.
Instructions for downloading eksctl can be found [here](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)
Instructions for setting up an EKS Cluster using eksctl can be found [here](https://discourse.prefect.io/t/how-to-create-a-kubernetes-cluster-on-aws-eks/1041)

### Deploying the Agent
The agent was deployed using the following [Discourse article](https://discourse.prefect.io/t/deploying-prefect-agents-on-kubernetes/1298) as a guide.

Secrets were created for the PREFECT_API_URL and the PREFECT_API_KEY (see third section of the above discourse post).

The work-queue name in the agent start command also got replaced by march-madness

### Docker Image


### Storage - S3
Create

### Execution Environment - KubernetesJob


### Basketball API


## What does this flow do?

This flow takes in data from a free API and uses some math to make semi-random predictions of the NCAA basketball championship games

The algorithm I came up with is fairly simple

## File Reference
- flow.py - main flow script that provides March Madness Predictions
- teams.json - json file that stores the RapidAPI id of each of the teams in the NCAA tournament as well as the id of their initial opponent
- Dockerfile - builds the image that is upload to ECR and used in the KubernetesJob block
- requirements.txt - dependencies for flow.py that are baked into the Docker image
- agent.yaml - the agent yaml file that contains all the config to run an agent in a Kubernetes cluster
- .prefectignore - this file is used to specify files that do not get uploaded to S3 storages



