# Helpful notes on using SCR

## Table of contents

1. [Introduction](#intro)
2. [Running with Docker Destop](#docker)
3. [Running in AzureContainer Instance](#aci)
4. [Running in Azure Web Application](#webapp)
5. [Running in a Kubernete Cluster](#k8s)
6. [Using it in Power Apps](#powerapps)

---

## Introduction<a name="intro"></a>

---

This document discusses some of the common usage patterns for SCR containers.
The documentation focuses on running SCR on Azure.

![image](SCRonAzure.png)

Prerequisites to using these notes:

### Recommended software

1. Docker Desktop <https://docs.docker.com/docker-for-windows/install/>. Take all the defaults during install.

2. Azure cli - <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli>. The document link  <https://docs.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest>

3. Scripting. You can use what you are comfortable with(python, curl, nodejs, etc.). A great tool for calls with no programming is Postman <https://www.postman.com/downloads/>.

### Environment setup

1. Make sure you have logged into Azure. If not, use this command: az login. Azure sessions have no timeout which is nice.
2. Create a ACR(Azure Container Registry) using the Azure portal.
3. Make sure your SCR image is pushed/published to that  ACR. You can setup ACR as a destination in SAS Viya.
4. Note the name and version of the container. You will need it to create a container.

In this documentation the following conventions are used.

1. The ACR is named scrdemosrgcr. (This results in a url of scrdemosrgcr.azurecr.io)
2. The documentation assumes that the published image is homeloan:0.1.0

Substitute these with your values.

## Running locally<a name="local"></a>

---

Once you have published the  SCR image to Azure or to any registry, you can test it locally by using the standard docker commands.

*FAQ on local repository: You might have to logon to the repository using docker login command <https://docs.docker.com/engine/reference/commandline/login/>*

To allow docker to access the ACR, issue this command

```sh
az acr login -n ACRname
ex:
az acr login -n scrdemosrgcr
```

Start the container with this command

```sh
docker run -p 8080:8080 {your-registry-url}/homeloan:0.1.0

Below are two examples:
docker run -p 8080:8080  scrdemosrgcr.azurecr.io/homeloan:0.1.0

docker run -p 8080:8080 acme.repository.com/homeloan:0.1.0

```

### `Data Points`

1. The docker image is in the repository is scrdemosrgcr.azurecr.io.
2. The image is named homeloan:0.1.0
3. The  API end point for the container is <http://localhost:8080/homeloan>

### A full session

```sh
az login
az acr login -n az acr login -n scrdemosrgcr
docker run -p 8080:8080 scrdemosrgcr.azurecr.io/homeloan:1.1
```

Below is a sample curl command to execute a score.

```sh

curl --location --request POST 'http://localhost:8080/homeloan' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data-raw ' {
    "inputs": [
        { "name": "CLAGE", "value": 94.36666667 },
        { "name": "CLNO", "value": 9 },
        { "name": "DEBTINC", "value": 0 },
        { "name": "DELINQ", "value": 0 },
        { "name": "DEROG", "value": 0 },
        { "name": "JOB", "value": "Other" },
        { "name": "LOAN", "value": 0 },
        { "name": "MORTDUE", "value": 25860 },
        { "name": "NINQ", "value": 1 },
        { "name": "REASON", "value": "HomeImp" },
        { "name": "VALUE", "value": 39025 },
        { "name": "YOJ", "value": 10.5 }
    ]
}
  
The output from this run is a JSON with the same schema as the input

{"outputs":[{"name":"AOV16_IMP_CLAGE","value":2.0},{"name":"AOV16_IMP_CLNO","value":3.0},{"name":"AOV16_IMP_DEBTINC","value":1.0},{"name":"AOV16_IMP_MORTDUE","value":1.0},{"name":"AOV16_IMP_VALUE","value":1.0},{"name":"AOV16_IMP_YOJ","value":5.0},{"name":"AOV16_LOAN","value":1.0},{"name":"BAD","value":null},{"name":"CLAGE","value":94.36666667},{"name":"CLNO","value":9.0},{"name":"DEBTINC","value":0.0},{"name":"DELINQ","value":0.0},{"name":"DEROG","value":0.0},{"name":"EM_CLASSIFICATION","value":"0 "},{"name":"EM_EVENTPROBABILITY","value":0.02692947290558756},{"name":"EM_PROBABILITY","value":0.9730705270944124},{"name":"GI_IMP_DELINQ_IMP_DEROG","value":5.0},{"name":"GI_IMP_DELINQ_IMP_JOB","value":6.0},{"name":"GI_IMP_DELINQ_IMP_NINQ","value":6.0},{"name":"GI_IMP_DELINQ_IMP_REASON","value":5.0},{"name":"GI_IMP_DEROG_IMP_JOB","value":6.0},{"name":"GI_IMP_DEROG_IMP_NINQ","value":6.0},{"name":"GI_IMP_DEROG_IMP_REASON","value":4.0},{"name":"GI_IMP_JOB_IMP_NINQ","value":7.0},{"name":"GI_IMP_JOB_IMP_REASON","value":2.0},{"name":"GI_IMP_NINQ_IMP_REASON","value":4.0},{"name":"G_IMP_DELINQ","value":3.0},{"name":"G_IMP_DEROG","value":3.0},{"name":"G_IMP_JOB","value":3.0},{"name":"G_IMP_NINQ","value":4.0},{"name":"IMP_CLAGE","value":94.36666667},{"name":"IMP_CLNO","value":9.0},{"name":"IMP_DEBTINC","value":0.0},{"name":"IMP_DELINQ","value":0.0},{"name":"IMP_DEROG","value":0.0},{"name":"IMP_JOB","value":"Other "},{"name":"IMP_MORTDUE","value":25860.0},{"name":"IMP_NINQ","value":1.0},{"name":"IMP_REASON","value":"HomeImp"},{"name":"IMP_VALUE","value":39025.0},{"name":"IMP_YOJ","value":10.5},{"name":"I_BAD","value":"0 "},{"name":"P_BAD0","value":0.9730705270944124},{"name":"P_BAD1","value":0.02692947290558756},{"name":"_WARN_","value":null},{"name":"clno_bin","value":null},{"name":"debtinc_bin","value":null},{"name":"equity_bin","value":null},{"name":"loan_bin","value":null},{"name":"PathID","value":"/2e69b523-3cb0-477f-966c-b33f93e3ddcd/a999c91d-478e-41f8-9da9-49e47063e0b3/4608e26d-5768-47c3-9ac3-25b505a3b4fe"},{"name":"ruleFiredFlags","value":null},{"name":"rulesFiredForRecordCount","value":null},{"name":"ruleFiredPathTraversal","value":null}]}


```

In deference to all the Python fans here is the same example in Python.

```python

import http.client
import json

conn = http.client.HTTPSConnection("localhost", 8080)
payload = json.dumps({
  "inputs": [
    {
      "name": "CLAGE",
      "value": 94.36666667
    },
    {
      "name": "CLNO",
      "value": 9
    },
    {
      "name": "DEBTINC",
      "value": 0
    },
    {
      "name": "DELINQ",
      "value": 0
    },
    {
      "name": "DEROG",
      "value": 0
    },
    {
      "name": "JOB",
      "value": "Other"
    },
    {
      "name": "LOAN",
      "value": 0
    },
    {
      "name": "MORTDUE",
      "value": 25860
    },
    {
      "name": "NINQ",
      "value": 1
    },
    {
      "name": "REASON",
      "value": "HomeImp"
    },
    {
      "name": "VALUE",
      "value": 39025
    },
    {
      "name": "YOJ",
      "value": 10.5
    }
  ]
})
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}
conn.request("POST", "/homeloan", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

```

Recommend you clean up your local docker after a test using standard docker commands.

---

## Running model in Azure Container Instance(ACI)<a name="aci"></a>

---

The quickest way to test your container on Azure is to run it as a Azure Container Instance.

## Creating an ACI Using Azure Portal

The basic steps are:

1. Select Container Instances
2. Select Create
3. Set the resource group.
4. Assign a meaningful name to your new container.
5. Under Image source select Azure Container Registry  and set the values.
6. Select Networking.
7. Set the desired DNS name label. *Strongly* recommend you chose a name that will make sense to your users. This will allow you to access the instance using a name instead of the public IP adddress.  
8. Under ports add 8080 since the SCR base container runs on this port.  **This is important**
9. Now create the instance.

Once it has completed you can access it from your scripts. The key point to remember is that the url for the container has the form ()

### URL for the ACI

The url for the ACI has the following syntax

Now you can access the application at <http://{dnslabel}.eastus.azurecontainer.io:8080>
So if in step 7 you used *homeloanaci* the final url will be something like this <http://homeloanaci.eastus.azurecontainer.io:8080/>
The eastus will be replaced by the region you choose to run the ACI.

### ACI Example

Below is a sample curl command.

```sh

curl --location --request POST 'http://homeloanci.eastus.azurecontainer.io:8080/homeloan' \
--header 'Content-Type: application/json' \
--data-raw ' {
         "CLAGE"  : 100, 
         "CLNO"   : 20,
         "DEBTINC": 20, 
         "DELINQ" : 2, 
         "DEROG"  : 0, 
         "JOB"    : "J1",  
         "LOAN"   : 1000,
         "MORTDUE": 4000,    
         "NINQ"   : 1, 
         "REASON" : "REFINANCE",
         "VALUE"  : 1000000,  
         "YOJ"    : 10
    
}
  '
```

A sample python code is below:

```py
import http.client
import json

conn = http.client.HTTPSConnection("homeloanaci.eastus.azurecontainer.io", 8080)
payload = json.dumps({
  "inputs": [
    {
      "name": "CLAGE",
      "value": 94.36666667
    },
    {
      "name": "CLNO",
      "value": 9
    },
    {
      "name": "DEBTINC",
      "value": 0
    },
    {
      "name": "DELINQ",
      "value": 0
    },
    {
      "name": "DEROG",
      "value": 0
    },
    {
      "name": "JOB",
      "value": "Other"
    },
    {
      "name": "LOAN",
      "value": 0
    },
    {
      "name": "MORTDUE",
      "value": 25860
    },
    {
      "name": "NINQ",
      "value": 1
    },
    {
      "name": "REASON",
      "value": "HomeImp"
    },
    {
      "name": "VALUE",
      "value": 39025
    },
    {
      "name": "YOJ",
      "value": 10.5
    }
  ]
})
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}
conn.request("POST", "/homeloan", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

---

## Running in Azure Web Application<a name="webapp"></a>

---
The Azure Portal makes it extremely easy to create Azure Web Applications. The steps are listed below for convenience

### Steps

1. From Azure Portal select App Services.
2. Select Create
3. Set your resource group name
4. Give a meaningful name for the instance. This will be the first part of the url for the web app.
5. Select Docker for publish
6. Select Linux for operating system
7. Select your region.
8. Either create Linux Plan or use an existing one.
9. For Sku and size select the Free F1 plan - that is all you need for demos
10. Select Next: Docker
11. In this second page select Azure Container Registry for image source
12. Complete setting your registry, image and Tag.
13. Select Review+create.
14. After the Azure app is up you have to set the WEBSITES_PORT variable to 8080 since the base image runs at this port

    - Select your web app from the list of Web Applications
    - Select Configurations from the explorer on the left.
    - Add WEBSITES_PORT with a value of 8080 as a new application setting
    - Let Azure restart the applications.

15. Once the restart has completed(takes a bit of time) your Azure app is ready to run.

### Accessing the web application

Your code will be similar to the previous examples. The url will be of the form

```text
    http://XXXX.azurewebsites.net/homeloan
    
    where XXXX is the label you specified in step 4 above.
    ex:
    http://homeloanapp.azurewebsites.net/homeloan
```

---

## Running in a Kubernete Cluster<a name="k8s"></a>

---

Assumption:

1. You have created a cluster using the Azure Portal. Make sure you have attached your container registry to this cluster

2. You have created a deployment.yaml in some directory(example below assumes it is called base). The sample yml file is shown below

```yml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: scrbase
  labels:
    app: scrbase
spec:
  replicas: 2
  selector:
    matchLabels:
      app: scrbase
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: scrbase
    spec:
      containers:
        - name: scrbase
          image: scrdemosrgcr.azurecr.io/homeloan:0.1.0
          imagePullPolicy: "Always"
          ports:
            - containerPort: 8080
          resources: {}
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: scrbase
  name: scrbase
spec:
  type: LoadBalancer
  ports:
    - port: 8080
      targetPort: 8080
  selector:
    app: scrbase

```

## Setup

This is not an essential step. I like to use a namespace for each of my models. This allows me to delete all the pods and services by simply deleting the namespace.  In the example below I am using scrdemo as the namespace. You can also run this in the default namespace.

```sh
kubectl create ns scrdemo
kubectl config set-context --current --namespace=scrdemo
```

## Simple deployment with a loadBalancer service

Change the image in the deployment.yaml to your container

Now create the instance.

```sh
cd base
kubectl apply -f deployment.yaml
```

Check and see if the pods are running

```sh
kubectl get pods

You should get something like this in the log

NAME                      READY   STATUS    RESTARTS   AGE
scrbase-8c8444b5c-6smjn   1/1     Running   0          12m
scrbase-8c8444b5c-crm4s   1/1     Running   0          12m

```

If the pod fails to initialize, then try this command to see what is going on

```sh
kubectl describe pod <name of the failing pod>
```

Most common error is using the wrong name of the image.

## Accessing the application

Issue this command to get the ip address of the service

```sh
kubectl get svc

You should see something like this:

NAME      TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)          AGE
scrbase   LoadBalancer   10.0.16.242   52.146.63.167   8080:31299/TCP   25m

```

Use the external-ip:8080 as the address of your container(52.0.16.242:8080).

---
