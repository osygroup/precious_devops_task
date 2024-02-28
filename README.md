# Precious DevOps Task
## Part II: Deliver Small App for K8S and a Helm Chart

This repository contains the following:
A simple Python HTTP app that upon query returns the contents of the Azure Blob Storage container in JSON format.
A Dockerfile for creation of a Docker image for the Python app
A Helm chart for the Python app
A workflow (update_helm_repo.yml) file for updating the Helm chart on the created Azure Storage Helm repository
A workflow (deploy_to_AKS.yml) file for building the Docker image, pushing it to Azure Container Registry, and installing the Python app Helm chart on AKS.


### 1. Create a simple HTTP app in the language of your choice that upon query returns the contents of the Azure Blob Storage in JSON format.
On the root of this repository is a simple Python HTTP app (app.py) that upon query returns the contents of the Azure Blob Storage container in JSON format when it is run.


### 2. Create a Dockerfile for the application
On the root of this repository is a Dockerfile for the creation of a Docker image for the Python app


### 3. Create a Helm chart to deploy the application to AKS cluster

Helm is the de facto package manager for Kubernetes and a chart is a collection of templates powered by a template engine that easily describes your Kubernetes manifest YAML files. Essentially Helm enables you to streamline your Kubernetes deployments by allowing you to use variables instead of hard-code values.


Create your Storage Account and container via Azure CLI, Terraform, or Azure Portal for the Helm repository.

Run the below commands to create Helm chart

```
mkdir chart-demo && cd chart-demo

helm create pythonapp_chart
```

cd to the created _pythonapp_chart_ directory, delete everything in the _templates_ folder and then add all your Kubernetes yaml files for the app inside the _templates_ folder. The default contents of the values.yaml file on the root of the _pythonapp_chart_ can be deleted and used to pass values into the chart. The values.yaml file in the helm chart in this repository is used to pass the docker image_name:tag value to the deployment.yaml file.
The deployment.yaml file in the chart has liveness and readiness probes to validate the application’s health.
Taken into account was the proper configuration of the application via the Helm chart as credentials details for the Azure Storage Blob Storage were stored in a secret.yaml file to prevent hard-coding of any credentials in the application's code. Credentials can further be managed properly using GitOps practices or credentials management services.

Run the following commands to examine the chart for possible issues
```
helm lint pythonapp_chart
```
Then run the below commands to package and prepare the chart for pushing to the Azure Storage Helm repository
```
helm package pythonapp_chart

helm repo index --url https://$storageAccountName.blob.core.windows.net/$containerName/ .
```
The 'helm package' command will create a tgz packaging of the chart
The 'helm repo index' command will create an index.yaml file in your working directory

Upload both files to the Azure Storage container (blob):
```
az storage blob upload --container-name $containerName --file index.yaml --name index.yaml --account-name $storageAccountName --account-key $storageAccountKey

az storage blob upload --container-name $containerName --file pythonapp_chart-0.1.0.tgz --name pythonapp_chart-0.1.0.tgz --account-name $storageAccountName --account-key $storageAccountKey
```
Add the helm repository to your local:
```
helm repo add helm_repo_azure https://helmdemo.blob.core.windows.net/helmdemo/
```
List all the repositories on your local:
```
helm repo list
```
Update all the helm repositories on your local:
```
helm repo update
```
To search the Helm repositories on your local for a chart (using a keyword):
```
helm search repo pythonapp
```

This repo contains a GitHub action workflow (.github/workflows/deploy_to_AKS.yml) file for building the Docker image, pushing it to Azure Container Registry, and installing the Python app Helm chart on an AKS cluster. The pipeline is triggered on push to the main branch.

View all the helm releases in the cluster:
```
helm list --all-namespaces
```
Port-forward the python app on your local (port 8099 in this case) to view the app:
```
kubectl port-forward -n pythonapp service/pythonapp 8099:5000
```
The Python app can now be reachable locally on a browser at http://localhost:8099/query

You can also create an ingress resource for access to the Python app over the internet


# Part IV: Helm Chart GitHub Action

This repo contains a GitHub action workflow (.github/workflows/update_helm_repo.yml) file for updating the Helm chart on the created Azure Storage Helm repository upon merge to the main branch. This pipeline packages the Python application’s Helm chart and pushes it to the Azure Storage Helm repository to update the chart.


