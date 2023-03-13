#!/usr/bin/env bash

set +x

eval $(minikube -p minikube docker-env)
minikube ssh "sudo -u root mkdir /postgres-data" || echo "DB folder already exists.skipping."
docker image build -t fastapi-poc-app:latest -f Dockerfile .
minikube kubectl create namespace fastapi || echo "Namespace fastapi already exists in the cluster"
helm install fastapi-service charts/fastapi-service/ --namespace fastapi || helm uninstall fastapi-service --namespace fastapi; sleep 10; helm install fastapi-service charts/fastapi-service/ --namespace fastapi
kubectl rollout status deployment fastapi-service --namespace fastapi --watch --timeout=2m || echo "Manual intervention required for the deployment, exiting..."
minikube service fastapi-service --url -n fastapi
