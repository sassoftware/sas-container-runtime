# SAS Container Runtime Tips

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Running Locally](#running-locally)
- [Running in Azure Container Instance (ACI)](#running-in-azure-container-instance-aci)
- [Running in Azure Web Application](#running-in-azure-web-application)
- [Running in a Kubernetes Cluster](#running-in-a-kubernetes-cluster)

## [Overview](#overview)

This document includes some common usage patterns for running SAS Container Runtime on Azure. The following figure provides a high-level representation of the process.

![image](SCRonAzure.png)

## [Prerequisites](#prerequisites)

### Recommended Software

- Docker Desktop <https://docs.docker.com/docker-for-windows/install/>. Take all the defaults during install.

- Azure CLI - <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli>. The document link  <https://docs.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest>

- Scripting. You can use what you are comfortable with(python, curl, nodejs, etc.). A great tool for calls with no programming is Postman <https://www.postman.com/downloads/>.

<!-- no toc -->
### Environment Setup

1. Confirm that you are logged in to Azure. If you are not, use this command: `az login` to log in. Azure sessions do not time out.
2. Create an Azure Container Registry (ACR) using the Azure portal.
3. Confirm that your SAS Container Runtime image is published to that ACR. (You can setup ACR as a destination in the SAS Viya platform.)
4. Note the name and version of the container. You need it to create a container.

In this section, the following conventions are used:

- The ACR is named *scrdemosrgcr*. This results in a url of *scrdemosrgcr.azurecr.io*.
- It is assumed that the published image is *homeloan:0.1.0*.

Substitute these with your values.

## [Running Locally](#running-locally)

---

Once you have published the SAS Container Runtime image to Azure (or to any registry), you can test it locally by using the standard Docker commands.

*FAQ on the local repository: You might have to log on to the repository using the Docker login command: <https://docs.docker.com/engine/reference/commandline/login/>*

To allow Docker to access the ACR, issue this command:

```sh
az acr login -n ACRname
```

For example:

```sh
az acr login -n scrdemosrgcr
```

Start the container using this command:

```sh
docker run -p 8080:8080 {your-registry-url}/homeloan:0.1.0
```

Here are two examples:

```sh
docker run -p 8080:8080  scrdemosrgcr.azurecr.io/homeloan:0.1.0

docker run -p 8080:8080 acme.repository.com/homeloan:0.1.0

```

#### Data Points

1. The Docker image is in the repository is scrdemosrgcr.azurecr.io.
2. The image is named homeloan:0.1.0
3. The  API end point for the container is <http://localhost:8080/homeloan>

#### A Full Session

```sh
az login
az acr login -n az acr login -n scrdemosrgcr
docker run -p 8080:8080 scrdemosrgcr.azurecr.io/homeloan:1.1
```

Here is a sample curl command to execute a score.

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

Here is the same example in Python.

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

It is recommended you clean up your local Docker after a test (using standard Docker commands).

---

## [Running in Azure Container Instance (ACI)](#running-in-azure-container-instance-aci)

---

The quickest way to test your container on Azure is to run it as an Azure Container Instance.

### Creating an ACI Using Azure Portal

Here are the basic steps:

1. Select **Container Instances**.
2. Select **Create**.
3. Set the resource group.
4. Assign a meaningful name to the new container.
5. For **Image source** select **Azure Container Registry**, and then assign the values.
6. Select **Networking**.
7. Set the desired DNS name label. It is strongly recommended you chose a name that is meaningful to your users. This enables you to access the instance using a name instead of the public IP address.  
8. Under **Ports** add *8080*. This is the port on which the SAS Container Runtime container runs.
9. Create the instance.

When complete, you can access the instance from your scripts. The URL for the container uses the form ().

#### URL for the ACI

Access the application at <http://{dnslabel}.eastus.azurecontainer.io:8080>

For example, if in Step 7 you used *homeloanaci* the final URL will be similar to the following:
 <http://homeloanaci.eastus.azurecontainer.io:8080/>

**Note**: *eastus* will be replaced by the region in which you choose to run the ACI.

##### ACI Example

Here is a sample curl command:

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

Here is sample Python code:

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

## [Running in Azure Web Application](#running-in-azure-web-application)

---
The Azure Portal makes it easy to create Azure Web Applications.

### Steps

1. In the Azure Portal select **App Services**.
2. Select **Create**.
3. Set your resource group name.
4. Specify a meaningful name for the instance. This will be the first part of the URL for the web app.
5. For Publish, select **Docker**.
6. For Operating System, select **Linux**.
7. Select your region.
8. Either create a Linux Plan or use an existing one.
9. For SKU and Size select the **Free F1** plan. This is all that you need for demos.
10. Select **Next: Docker**.
11. On the second page, select **Azure Container Registry** for **Image Source**.
12. Complete the process to set your Registry, Image and Tag.
13. Select **Review+create**.
14. After the Azure app is up, set the **WEBSITES_PORT** variable to 8080. The SAS Container Runtime image runs at this port.

    - Select your web app from the list of Web Applications.
    - Select **Configurations** from the explorer on the left.
    - Add **WEBSITES_PORT** and assign a value of 8080 as a new application setting.
    - Allow Azure to restart the applications.

15. When the restart is complete (this can take a while), your Azure app is ready to run.

#### Accessing the Web Application

Your code will be similar to the previous examples. The URL will be of the form:

```text
    http://XXXX.azurewebsites.net/homeloan
```

where XXXX is the label that you specified in step 4 above.

For example:

```text
    http://homeloanapp.azurewebsites.net/homeloan
```

---

## [Running in a Kubernetes Cluster](#running-in-a-kubernetes-cluster)

---

Assumptions:

1. You created a cluster using the Azure Portal. Make sure that you attached your container registry to this cluster.

2. You created a deployment.yaml file in a directory. A sample yaml file is shown below.

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

### Setup

**Note**: This is not an essential step.

Using a namespace for each of model enables you to delete all the pods and services by simply deleting the namespace. In the example below, scrdemo is the namespace. You can also run this in the default namespace.

```sh
kubectl create ns scrdemo
kubectl config set-context --current --namespace=scrdemo
```

### Simple Deployment with a loadBalancer Service

Change the image in the **deployment.yaml** to your container and then create the instance:

```sh
cd base
kubectl apply -f deployment.yaml
```

Check to see whether the pods are running:

```sh
kubectl get pods
```

You should see something similar to the following in the log:

```sh
NAME                      READY   STATUS    RESTARTS   AGE
scrbase-8c8444b5c-6smjn   1/1     Running   0          12m
scrbase-8c8444b5c-crm4s   1/1     Running   0          12m
```

If the pod fails to initialize, use this command to learn more:

```sh
kubectl describe pod <name of the failing pod>
```

**Note**: The most common error is using the wrong image name.

### Accessing the Application

Use this command to obtain the IP address of the service:

```sh
kubectl get svc
```

You should see something similar the following:

```sh
NAME      TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)          AGE
scrbase   LoadBalancer   10.0.16.242   52.146.63.167   8080:31299/TCP   25m
```

Use  *external-ip*:*8080* as the address of your container (52.0.16.242:8080).

---
