# Configure Authentication for SAS Container Runtime in Azure Active Directory

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Creating an Azure AKS Cluster](#creating-an-aks-cluster)
- [Setting Up SAS Container Runtime in an Azure Cluster](#setting-up-sas-container-runtime-in-an-azure-cluster)
  - [Deploy SAS Container Runtime in the Cluster](#deploy-sas-container-runtime-in-the-cluster)
  - [Create a Public IP and DNS Label for the SAS Container Runtime API](#create-a-public-ip-and-dns-label-for-the-sas-container-runtime-api)
- [Create an Ingress Controller](#create-an-ingress-controller)
- [Access the SAS Container Runtime API without Security](#access-the-sas-container-runtime-api-without-security)
- [Securing the SAS Container Runtime API](#securing-the-sas-container-runtime-api)
  - [Install Cert-Manager](#install-cert-manager)
  - [Create Azure AD Registration for the SAS Container Runtime Endpoint](#create-azure-ad-registration-for-a-sas-container-runtime-endpoint)
  - [Create an oauth2 Authentication Proxy](#create-an-oauth2-authentication-proxy)
  - [Create a Certificate Object](#create-a-certificate-object)
  - [Add Ingress Routes for Proxy and SAS Container Runtime](#add-ingress-routes-for-proxy-and-sas-container-runtime)
  - [Register the Client Application in Azure AD](#register-the-client-application-in-azure-ad)
  - [Get an Access Token for the SAS Container Runtime API using the Registered Client](#get-an-access-token-for-the-sas-container-runtime-api-using-the-registered-client)
  - [Access the SAS Container Runtime API with Access Token](#access-the-sas-container-runtime-api-with-an-access-token)

## Overview

SAS Container Runtime does not have built in authentication support. When deployed in a Kubernetes cluster, an authentication provider can use a sidecar proxy. This example shows how to configure Azure Active Directory (AD) authentication for SAS Container Runtime using NGINX proxy in an AKS cluster.

## Prerequisites

- Azure CLI
- Helm

## Creating an AKS Cluster

Create a resource group by using the `az group create` command:

```Azure CLI
az group create --name myResourceGroup --location eastus
```

Create an AKS cluster by using the `az aks create` command. The following example creates a cluster named myAKSCluster with one node:

```Azure CLI
az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 1
```

If you already have an AKS cluster, note the resource group that is associated with the cluster by using the `az aks` command:

```Azure CLI
az aks show --resource-group myResourceGroup --name myAKSCluster --query nodeResourceGroup -o tsv
```

## Setting Up SAS Container Runtime in an Azure Cluster

### Deploy SAS Container Runtime in the Cluster

This procedure assumes that you already have a SAS Container Runtime Docker image available in an Azure registry.

1. Give permission to pull an image from the registry using the `az aks update` command. Assuming the Docker image for SAS Container Runtime is available in myAzureRegistry, the following command attaches the registry to the AKS cluster in previous step:

    ```sh
    az aks update -n myAKSCluster -g myResourceGroup --attach-acr myAzureRegistry
    ```

2. Create a SAS Container Runtime deployment and corresponding Kubernetes service object. Here is a sample template:

    ```sh
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

3. Create the issuer, using the `kubectl apply` command:

    ```sh
    kubectl apply -f scr-manifest.yaml --namespace scr
    ```

### Create a Public IP and DNS Label for the SAS Container Runtime API

Create a public IP address with the static allocation method using the `az network public-ip create` command.

The following example creates a public IP address that is named scr-demo-ip in the AKS cluster resource group obtained in the previous step. It  associates dnslabel scr-demo.eastus.cloudapp.azure.com with the IP address.

```Azure CLI
az network public-ip create --resource-group MC_myResourceGroup_myAKSCluster_eastus --name scr-demo-ip --sku Standard --allocation-method static  --dns-name scr-demo --query publicIp.ipAddress -o tsv
```

## Create an Ingress Controller

Now deploy the nginx-ingress chart with Helm.

1. You must pass two additional parameters to the Helm release. These parameters ensure that the Ingress controller is aware of the following:

   - the static IP address of the load balancer to be allocated to the ingress controller service.
   - the DNS name label that is applied to the public IP address resource.

2. For the HTTPS certificates to work correctly, a DNS name label is used to configure an FQDN for the Ingress controller IP address.

   - Add the `--set controller.service.loadBalancerIP` parameter. Specify your own public IP address that was created in the previous step.
   - Add the `--set controller.service.annotations."service\.beta\.kubernetes\.io/azure-dns-label-name"` parameter.
   - Specify a DNS name label to be applied to the public IP address that was created in the previous step.

3. The Ingress controller also needs to be scheduled on a Linux node. Windows server nodes should not run the Ingress controller.
  
   Specify a node selector by using the `--set nodeSelector` parameter. This instructs the Kubernetes scheduler to run the NGINX Ingress controller on a Linux node. Use the IP address and DNS label that were created in the previous step for STATIC-IP and DNS-LABEL parameters. Here is an example:

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

When the Kubernetes load balancer service is created for the NGINX Ingress controller, your static IP address is assigned, as shown in the following example output:

```sh
$ kubectl --namespace scr get services -o wide -w nginx-ingress-ingress-nginx-controller

NAME                                     TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)                      AGE   SELECTOR
nginx-ingress-ingress-nginx-controller   LoadBalancer   10.0.74.133   EXTERNAL_IP     80:32486/TCP,443:30953/TCP   44s   app.kubernetes.io/component=controller,app.kubernetes.io/instance=nginx-ingress,app.kubernetes.io/name=ingress-nginx
```

The Ingress controller is now accessible through the IP address or the FQDN derived from the DNS label.

## Access the SAS Container Runtime API without Security

With the public IP, the NGINX Ingress controller can be routed to access the API without any security. Here is a sample yaml file:

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

There is neither authentication nor transport layer security now. You can verify SAS Container Runtime API access using a curl command:

```curl
 curl http:<DNS_LABEL>/__env
```

## Securing the SAS Container Runtime API

To secure the SAS Container Runtime API, you must authenticate requests to the API endpoint and secure the transport. SAS Container Runtime does not have a built-in security layer. Security is added by using a sidecar that authenticates requests to the SAS Container Runtime API endpoint. The sidecar provides the following functionality:

- TLS termination for API requests
- Authentication of incoming requests

### Install Cert-Manager

The NGINX ingress controller supports TLS termination. This example uses a self-signed certificate using cert-manager. To install the cert-manager controller in a Kubernetes RBAC-enabled cluster, use the following `helm install` command:

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

Before certificates can be issued, cert-manager requires an Issuer or ClusterIssuer resource. These Kubernetes resources are identical in functionality, however Issuer works in a single namespace and ClusterIssuer works across all namespaces. For more information, see the cert-manager issuer documentation.

Create a cluster issuer, such as cluster-issuer.yaml, using the following example manifest. Update the email address with a valid address for your organization:

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

To create the issuer, use the `kubectl apply` command:

```sh
kubectl apply -f cluster-issuer.yaml --namespace scr
```

### Create Azure AD Registration for a SAS Container Runtime Endpoint

Here are the steps to register the endpoint that you use as a resource in Azure AD:

1. In the Azure portal, select **Active Directory** > **App registrations** > **New registration**.
  
   On the **Register an application** page, enter a name for your app registration (scr-demo).
   For the **Redirect URI**, enter the value <https://{DNS_LABEL}.eastus.cloudapp.azure.com/oauth2/callback> and then select **Create**.

2. After the app registration is created, note the values of **Application (client) ID** (APPLICATION_ID) and **Directory (tenant) ID**. (TENANT_ID).

3. Select **Certificates & secrets** > **New client secret** > **Add**. 

   Copy the client secret value that appears on the page (APPLICATION_SECRET). It is not displayed again.

4. Open the manifest and set the **accessTokenAcceptedVersion** property to *2*.

5. Save the changes.

### Create an Oauth2 Authentication Proxy

This section shows to how use an NGINX proxy for authentication with Azure AD before requests are redirected to SAS Container Runtime.

In this example, an oauth2 proxy is available at bitnami/oauth2-proxy:latest.

Configure the proxy with the APPLICATION_ID, TENANT_ID, and APPICATION_SECRET parameters from the previous step.

Create the COOKIE_SECRET value by running the following Docker command. (This is used for interactive clients.)

```sh
 docker run -ti --rm python:3-alpine python -c 'import secrets,base64; print(base64.b64encode(base64.b64encode(secrets.token_bytes(16))));'
```

Here is the template yaml file for the oauth2 proxy:

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

### Create a Certificate Object

Create a certificate to secure the DNS name. Use the fully qualified domain name (FQDN), for example, scr-api.eastus.cloudap.azure.com.

Here is an example template yaml file:

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

### Add Ingress Routes for Proxy and SAS Container Runtime

A new Ingress is added to route unauthenticated clients to the oauth2 proxy service. Ingresses have a tls section. The certificate that was created in the previous steps is used.

Use the FQDN for the host in the tls section and the rules section.

A sample template is below. The annotations on NGINX proxy direct unauthenticated requests to the /oauth2 path. The ingress for the oauth2 path directs the requests to the oauth2 proxy. The proxy is configured to validate the access token, verify the issuer, and claim it on the API. If the validation is successful, the request is directed to SAS Container Runtime container.

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

### Register the Client Application in Azure AD

To get an access token, the client should be registered in Azure AD as follows:

1. In the Azure portal, select **Active Directory** > **App registrations** > **New registration**.

   On the **Register an application** page, enter a name for your app registration (scr-client).

   **Note**: A Redirect URI is not needed for daemon clients.

2. After the application registration is created, note the value of **Application (client) ID**. (APPLICATION_ID) and **Directory (tenant) ID**. (TENANT_ID).

3. Select **Certificates & secrets** > **New client secret** > **Add**.
  
   Copy the client secret value shown in the page (APPLICATION_SECRET). It does not appear again.

4. Open the manifest and set the **accessTokenAcceptedVersion** property to *2*.

5. Save the changes.

### Get an Access Token for the SAS Container Runtime API Using the Registered Client

Get an access token using the curl command. 

- Use the APPLICATION_ID and APPLICATION_SECRET of client. 
- Use the APPLICATION_OF server as scope.

Here is an example:

```Curl for acccess token
curl -X POST https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token \
       -F grant_type=client_credentials \
       -F client_secret=<APPLICATION_SECRET> \
       -F scope=<APPLICATION_ID of SERVER>/.default \
       -F client_id=<APPLICATION_ID of client from previous step>
```

### Access the SAS Container Runtime API with an Access Token

Pass the access token that was obtained in previous steps as the bearer token to call the API. Here is an example:

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

