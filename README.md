# precious_devops_task

mkdir chart-test && cd chart-test

helm create myfirstchart

helm lint pythonapp_chart

helm package pythonapp_chart

helm repo index --url https://helmdemo.blob.core.windows.net/helmdemo/ .

The 'helm package' command will create a tgz packaging of the chart
The 'helm repo index' command will create an index.yaml file in your working directory

az storage blob upload --container-name helmdemo --file index.yaml --name index.yaml --account-name helmdemo --account-key $storageAccountKey

az storage blob upload --container-name helmdemo --file pythonapp_chart-0.1.0.tgz --name pythonapp_chart-0.1.0.tgz --account-name helmdemo --account-key $storageAccountKey

At some point, you will want to upload additional charts. For each new chart, you’ll need to regenerate the index.yaml file. You can use the command helm repo index --url to rebuild your index.yaml, this will rebuild it from scratch and by default will only include the charts found locally. 
So ensure that you are creating your new charts in the same directory with others, so that the index.yaml file will capture all the charts. If you create a new chart in a different directory, the index.yaml file that will be generated will only capture that new chart. Uploading this file on the Azure storage container (the private Helm repository) will overwrite whatever index.yaml file that is already there and render the earlier uploaded packaged charts useless. A local update of Helm repos will remove the charts.

Add the helm repository to your local:
To add a Helm repo to your local:
helm repo add helm_repo_azure https://helmdemo.blob.core.windows.net/helmdemo/

List all the repositories on your local:
helm repo list

Update all the helm repositories on your local:
helm repo update

To search the Helm repositories on your local for a chart (using a keyword):
helm search repo pythonapp

View all the helm releases in the cluster:
helm list --all-namespaces

Port-forward the python app on your local (port 8099 in this case) to view the app:
kubectl port-forward -n pythonapp service/pythonapp 8099:5000
