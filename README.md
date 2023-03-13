# fastapi-poc


An example for Fast API with Auth0 RBAC authentication to perform a jumble of random string and audit all responses from the api.

Jumble API, Audit API Example

## Table of Contents

* [Preconditions](#preconditions)
* [Run Local Install](#runlocalinstall)
* [Run With Docker](#Run With Docker)
* [Run with Minicube](#Run with Minicube)
* [Authentication using Auth0](#Authentication using Auth0)
* [Access API Endpoint](#Access API Endpoint)
* [Notes](#notes)

## Preconditions:

- Python 3
- Minikube
- Docker
- Helm

## Clone the project

```
git clone https://github.com/nidhinnru/fastapi-poc
```

## Run Local Install

### Install dependencies

```
make localinstall
```
or 
```
  $virtualenv dev
  $source dev/bin/activate
  $pip install -r requirements
  $uvicorn app.main:app --host 0.0.0.0 --port 8000
```
### Run server

```
make local_run_app
```

### Run test - ToDo

```
make test
```

## Run With Docker

### Run server

```
make docker_build
```

### Run test - ToDo

```
make docker_test
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8000/docs
```

## Run with Minicube

### A helm chart is prepared for FastAPI & Postgresql deployment. 

### Getting started with Kubernetes

1. Starting the Minikube

```bash
minikube start
```
2. To start the entire process

```
make run
```
This will execute the following: 
* A local folder for persistent volume inside minikube will be created under /postgres-data.
* Run the docker build & create image locally.
* Create a "fastapi" kubeneretes namespace.
* Check if there are any dangling helm charts, uninstall & reinstall the helm chart.
* Verify the status of the "fastapi-service" deployment.
* Print the endpoint of the FastAPI service endpoint. 

3. Now, explore to the API!

Go to http://example.api/docs

4. Once done, stop and delete Minikube!

```bash
minikube stop; minikube delete
```

### Useful Commands

Get Kubernetes Deployments and Pods

```bash
kubectl get deployments
kubectl get pods
```
## Authentication using Auth0

### RBAC Setup
Setup is configured as per https://developer.auth0.com/resources/code-samples/api/fastapi/basic-role-based-access-control

To initiate a new session
```bash
make get_endpoint
```

To get the Json Web Token(JWT), it is expected to send a post request using "client_credentials" as grant type. client_id & client_secret can be collected from the auth0 API application portal. 

```bash
curl --request POST   --url https://dev-vahuhjbwf4lzeonj.us.auth0.com/oauth/token   --header 'content-type: application/json'   --data '{"client_id":"*********","client_secret":"*******","audience":"http://127.0.0.0:8002","grant_type":"client_credentials"}'
```

Export the output of the above results into an environment variable(Only for local development)

```bash
export TOKEN=*************
```

## Access API Endpoints

### Jumble a random string

Send a post response with a string payload to "/jumble" path to return a jumbled string.

```bash
curl -s --request POST --url http://<<API-ENDPOINT-URL>>/jumble -d 'Dummy FastAPI' --header "authorization: Bearer $TOKEN"
```

### Audit Response

All incoming requests to the API will be stored in the database for audit purpose and the last 10 api response results can be retrieved. 

```bash
curl -s --request GET --url http://<<API-ENDPOINT-URL/audit --header "authorization: Bearer $TOKEN"
```

## Notes

* Setup of this API is very minimalistic as far as Jumble & Audit API is concerned.
* Test cases - TBD
* Latency can be reduced by adding a Redis cache to this setup.
* Persistent storage is available for postgres, since this setup uses minikube, node affinity configuration is required in PV.
* Goal of the RBAC is to restrict the normal users accessing "/audit" endpoint. Multiple roles can be created in Auth0 portal & permissions can be assigned & validated in the method requests. 
* Setup is tested locally in Window OS.
