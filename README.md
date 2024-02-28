# precious_devops_task

View all the helm releases in the cluster:
helm list --all-namespaces

Port-forward the python app on your local (port 8099 in this case) to view the app:
kubectl port-forward -n pythonapp service/pythonapp 8099:5000
