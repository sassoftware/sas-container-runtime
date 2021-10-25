# Configure Authentication for SAS Container Runtime (SCR) in Azure AD

## Overview

SAS Container Runtime does not have builtin authentication support. When deployed in kubernetes cluster, we can plugin authentication provider using side car proxy. This example shows how to configure Azure AD authentication for SCR using nginx proxy in AKS cluster.

## Prerequisites

- Azure CLI \*
- Helm

## Creating Azure AKS Cluster

Create a resource group using the az group create command.

```Azure CLI
az group create --name myResourceGroup --location eastus
```

Create an AKS cluster using the az aks create command. The following example creates a cluster named myAKSCluster with one node:

```Azure CLI
az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 1
```

If you already have an AKS Cluster note down the resoure group associated with the cluster using az aks command.

```Azure CLI
az aks show --resource-group myResourceGroup --name myAKSCluster --query nodeResourceGroup -o tsv
```

## Setup SCR in Azure cluster

### Deploy SCR in the Cluster

This step assumes you already have SCR available as docker image in azure registry.
First give permission to pull image from the registry using az aks update command. Assuming the dokcer image for SCR is available in myAzureRegistry, the following command attaches the regsitry to the AKS cluster in previous step.

```sh
az aks update -n myAKSCluster -g myResourceGroup --attach-acr myAzureRegistry
```

Create and SCR deployment and corresponding kubernetes service object. Here is the sample template.

```scr-manifest.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sas-decisions-runtime
  labels:
    app: sas-decisions-runtime
  name: sas-decisions-runtime
  namespace: scr


spec:
  selector:
    matchLabels:
      app: sas-decisions-runtime
  template:
    metadata:
      labels:
        app: sas-decisions-runtime
    spec:
      containers:
      - name: sas-decisions-runtime
        image: myAzureRegistry.azurecr.io/sas-decisions-runtime:latest
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: sas-decisions-runtime-service
  namespace: scr
spec:
  ports:
  - name: http
    port: 8080
  selector:
    app: sas-decisions-runtime
  type: ClusterIP
```

To create the issuer, use the kubectl apply command.

```sh
kubectl apply -f scr-manifest.yaml --namespace scr
```

### Creating public IP and dns label for SCR API

create a public IP address with the static allocation method using the az network public-ip create command. The following example creates a public IP address named scr-demo-ip in the AKS cluster resource group obtained in the previous step and associate dnslabel scr-demo.eastus.cloudapp.azure.com with the ip address:

```Azure CLI
az network public-ip create --resource-group MC_myResourceGroup_myAKSCluster_eastus --name scr-demo-ip --sku Standard --allocation-method static  --dns-name scr-demo --query publicIp.ipAddress -o tsv
```

## Create an Ingress Controller

Now deploy the nginx-ingress chart with Helm. You must pass two additional parameters to the Helm release so the ingress controller is made aware both of the static IP address of the load balancer to be allocated to the ingress controller service, and of the DNS name label being applied to the public IP address resource. For the HTTPS certificates to work correctly, a DNS name label is used to configure an FQDN for the ingress controller IP address.

Add the --set controller.service.loadBalancerIP parameter. Specify your own public IP address that was created in the previous step.
Add the --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-dns-label-name" parameter. Specify a DNS name label to be applied to the public IP address that was created in the previous step.
The ingress controller also needs to be scheduled on a Linux node. Windows Server nodes shouldn't run the ingress controller. A node selector is specified using the --set nodeSelector parameter to tell the Kubernetes scheduler to run the NGINX ingress controller on a Linux-based node. Use the IP address and dns label created in the previous step for STATIC-IP and DNS-LABEL parameters in the following snippet.

```Azure CLI
# Create a namespace for your ingress resources
kubectl create namespace scr

# Add the ingress-nginx repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

# Use Helm to deploy an NGINX ingress controller
helm install nginx-ingress ingress-nginx/ingress-nginx \
    --namespace scr \
    --set controller.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set defaultBackend.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set controller.admissionWebhooks.patch.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set controller.service.loadBalancerIP="STATIC_IP" \
    --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-dns-label-name"="DNS_LABEL"
```

When the Kubernetes load balancer service is created for the NGINX ingress controller, your static IP address is assigned, as shown in the following example output:

```sh
$ kubectl --namespace scr get services -o wide -w nginx-ingress-ingress-nginx-controller

NAME                                     TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)                      AGE   SELECTOR
nginx-ingress-ingress-nginx-controller   LoadBalancer   10.0.74.133   EXTERNAL_IP     80:32486/TCP,443:30953/TCP   44s   app.kubernetes.io/component=controller,app.kubernetes.io/instance=nginx-ingress,app.kubernetes.io/name=ingress-nginx
```

The ingress controller is now accessible through the IP address or the FQDN specified derived from DNS label.

## Access SCR API without security

Now that we have public ip, we can use add route to nginx ingress controller to access the API without any security. Here is yaml

```nginx-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: scr-echo-ingress
  namespace: scr
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
  - host: scr-demo.eastus.cloudapp.azure.com
    http:
      paths:
      - path: /(.*)
        pathType: Prefix
        backend:
          service:
            name: sas-decisions-runtime-service
            port:
              number: 8080

```

You can verify SCR api access with curl now. There is neither authentication nor transportlayer security now.

```curl
 curl http:<DNS_LABEL>/__env
```

## Securing SCR API

To Secure SCR API, we need authenticate requestes to the API end point and also secure the transport. SCR does not have any builtin security layer. Security added by plugging in a side car that autenticates request to SCR API end point. Side car provides the following :

- TLS termination for API requests
- Authenticate the incoming requests with

### Install Cert-manager

The NGINX ingress controller supports TLS termination. For this example we use self signed certiciate using cert manager. To install the cert-manager controller in an Kubernetes RBAC-enabled cluster, use the following helm install command:

```console
# Label the cert-manager namespace to disable resource validation
kubectl label namespace ingress-basic cert-manager.io/disable-validation=true

# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
helm repo update

# Install the cert-manager Helm chart
helm install \
  cert-manager \
  --namespace ingress-basic \
  --version v1.3.1 \
  --set installCRDs=true \
  --set nodeSelector."beta\.kubernetes\.io/os"=linux \
  jetstack/cert-manager
```

Before certificates can be issued, cert-manager requires an Issuer or ClusterIssuer resource. These Kubernetes resources are identical in functionality, however Issuer works in a single namespace, and ClusterIssuer works across all namespaces. For more information, see the cert-manager issuer documentation.

Create a cluster issuer, such as cluster-issuer.yaml, using the following example manifest. Update the email address with a valid address from your organization:

```yaml
apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: tls-secret
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: user@contoso.com
    privateKeySecretRef:
      name: letsencrypt-staging
    solvers:
      - http01:
          ingress:
            class: nginx
            podTemplate:
              spec:
                nodeSelector:
                  "kubernetes.io/os": linux
```

To create the issuer, use the kubectl apply command.

```sh
kubectl apply -f cluster-issuer.yaml --namespace scr
```

### Create Azure AD Registration for SCR endpoint

To protect the API, end point should be registered as a resource in Azure AD

Here are the steps:

1. In the Azure portal, select Active Directory > App registrations > New registration.
   In the Register an application page, enter a Name for your app registration (scr-demo).
   For the Redirect URI enter the value <https://{DNS_LABEL}.eastus.cloudapp.azure.com/oauth2/callback> and then Select Create.
2. After the app registration is created, note down the value of **Application (client) ID**. (APPLICATION_ID) and **Directory (tenant) ID**. (TENANT_ID).
3. Select Certificates & secrets > New client secret > Add. Copy the client secret value shown in the page (APPLICATION_SECRET). It won't be shown again.
4. Open the manifest and set **accessTokenAcceptedVersion** property to 2. Save the changes.

### Create oauth2 Authentication Proxy

Here we ae using nginx proxy to do authentication with Azure AD before requests are redirected to SCR. In this example we are using oauth2 proxy available at bitnami/oauth2-proxy:latest. Configure the proxy with APPLICATION_ID, TENANT_ID and APPICATION_SECRET paraneters from previous step. Create COOKIE_SECRET value created by running this docker command ( This is used for interactive clients )

```sh
 docker run -ti --rm python:3-alpine python -c 'import secrets,base64; print(base64.b64encode(base64.b64encode(secrets.token_bytes(16))));'
```

Here is the template yaml for oauth2 proxy

```oauth2 yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    k8s-app: oauth2-proxy
  name: oauth2-proxy
  namespace: scr
spec:
  replicas: 1
  selector:
    matchLabels:
      k8s-app: oauth2-proxy
  template:
    metadata:
      labels:
        k8s-app: oauth2-proxy
    spec:
      containers:
      - args:
        - '--provider=azure'
        - '--azure-tenant=<TENANT_ID>'
        - '--skip-jwt-bearer-tokens=true'
        - --oidc-issuer-url=https://sts.windows.net/<TENANT_ID>/
        - --extra-jwt-issuers=https://login.microsoftonline.com/<TENANT_ID>/v2.0=<APPLICATION_ID>
        - '--request-logging=true'
        - '--auth-logging=true'
        - '--standard-logging=true'
        - --email-domain=*
        - --upstream=file:///dev/null
        - --http-address=0.0.0.0:4180
        # Register a new application
        # https://github.com/settings/applications/new
        env:
        - name: OAUTH2_PROXY_CLIENT_ID
          value: <APPLICATION_ID>
        - name: OAUTH2_PROXY_CLIENT_SECRET
          value: <APPLICATION_SECRET>
        # docker run -ti --rm python:3-alpine python -c 'import secrets,base64; print(base64.b64encode(base64.b64encode(secrets.token_bytes(16))));'
        - name: OAUTH2_PROXY_COOKIE_SECRET
          value: eaBamVtoeWCVmNt9/W4dNQ==
        image: bitnami/oauth2-proxy:latest
        imagePullPolicy: Always
        name: oauth2-proxy
        ports:
        - containerPort: 4180
          protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  labels:
    k8s-app: oauth2-proxy
  name: oauth2-proxy
  namespace: ingress-basic
spec:
  ports:
  - name: http
    port: 4180
    protocol: TCP
    targetPort: 4180
  selector:
    k8s-app: oauth2-proxy
```

### Create certicate object

Create certifcate to secure the dns name. Use thefully qualiufied dns name (FQDN) such as scr-api.eastus.cloudap.azure.com. Here is the template

```certiftate.yaml
apiVersion: cert-manager.io/v1alpha2
kind: Certificate
metadata:
  name: tls-secret
  namespace: ingress-basic
spec:
  secretName: tls-secret
  dnsNames:
  - <FQDN>
  acme:
    config:
    - http01:
        ingressClass: nginx
      domains:
      - <FQDN>
  issuerRef:
    name: letsencrypt-staging
    kind: ClusterIssuer
```

### Add ingress routes for proxy and scr

> New ingress is added to route unauthenticated clients to ozuth2 proxy service. Ingreses have tls section and the certicate created in the previous steps is used. Use the FQDN for the host in the tls section and rules section. Here is the template. The annotaions on nginx proxy directs unautenticated requests to /oauth2 path. The inngress for oauth2 path directs the requests to oauth2 proxy. The proxy is configued to validate acess token and verify the issuer and claim it has on the API. If the validation is successful request is directed to SCR container.

```routes.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: scr-echo-ingress
  namespace: scr
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-staging
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
    nginx.ingress.kubernetes.io/auth-url: "https://$host/oauth2/auth"
    nginx.ingress.kubernetes.io/auth-signin: "https://$host/oauth2/start?rd=$escaped_request_uri"

spec:
  tls:
  - hosts:
    - scr-api1.eastus.cloudapp.azure.com
    secretName: tls-secret
  rules:
  - host: <FQDN>
    http:
      paths:
      - path: /(.*)
        pathType: Prefix
        backend:
          service:
            name: sas-decisions-runtime-service
            port:
              number: 8080

---

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: oauth2-proxy-ingress
  namespace: scr
spec:
  rules:
  - host: <FQDN>
    http:
      paths:
      - backend:
          service:
            name: oauth2-proxy
            port:
              number: 4180
        path: /oauth2
        pathType: Prefix
  tls:
  - hosts:
    - <FQDN>
    secretName: tls-secret
```

### Register client application in Azure AD

To get acdess token, ciient should be registred in Azure AD.
Here are the steps:

1. In the Azure portal, select Active Directory > App registrations > New registration.
   In the Register application page, enter a Name for your app registration (scr-client).
   No Redirect URI is needed for daemon clients.
2. After the app registration is created, note down the value of **Application (client) ID**. (APPLICATION_ID) and **Directory (tenant) ID**. (TENANT_ID).
3. Select Certificates & secrets > New client secret > Add. Copy the client secret value shown in the page (APPLICATION_SECRET). It won't be shown again.
4. Open the manifest and set **accessTokenAcceptedVersion** property to 2. Save the changes.

### Get access token for SCR API using the registered client

Get an access token using the curl command using APPLICATION_ID and APPLICATION_SECRET of client and using APPLICATION_OF server as scope.

```Curl for acccess token
curl -X POST https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token \
       -F grant_type=client_credentials \
       -F client_secret=<APPLICATION_SECRET> \
       -F scope=<APPLICATION_ID of SERVER>/.default \
       -F client_id=<APPLICATION_ID of client from previous step>
```

### Access SCR API with access token

Pass the Access token obtained in previous steps as Beater token to call the API.

```Curl
curl --location --request POST 'https://scr-demo.eastus.cloudapp.azure.com/echo_test/executescalarecho' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <ACCESS_TOKEN>' \
--data-raw '{
	"inputs": [
		{
			"name": "i",
			"value": 100
		}
	]
}
```
