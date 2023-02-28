# March Madness 2023 Predictions powered by Prefect
## This is a repo to store Prefect flow code for March Madness 2023 predictions

## Setting up the Infrastructure

### EKS Cluster

This workload does not require a complicated setup, so I decided to use eksctl to create the cluster in AWS

### Deploying the Agent
### Docker Image
### Storage - S3
### Execution Environment - KubernetesJob
### Basketball API

## What does this flow do?

## File Reference
- flow.py - main flow script that provides March Madness Predictions
- get_league.py - script to get the league id for the NCAA from the Basketball API. This is not used in flow.py and the league id is hard coded in the flow
- Dockerfile - builds the image that is upload to ECR and used in the KubernetesJob block
- requirements.txt - dependencies for flow.py that are baked into the Docker image
- agent.yaml - the agent yaml file that contains all the config to run an agent in a Kubernetes cluster
- .prefectignore - this file is used to specify files that do not get uploaded to S3 storage



