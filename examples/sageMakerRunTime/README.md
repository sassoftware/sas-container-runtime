# SCR - SAS model scoring on AWS SageMaker

<blockquote>
SageMaker Hosting services provides runtime for custom model containers. Customers looking for guidance can follow undermentioned approach to deploy SAS models to SageMaker Hosting services. SAS SCR OCI models need a few tweaks before they can run on AWS SageMaker and this solution helps.

</blockquote>

## Motivation for using SageMaker Runtime

Customers who are already using AWS SageMaker for all runtime scoring may prefer to use same for SAS SCR models. Moreover SageMaker Hosting services provide auto-scaling, model invocation stats that may be useful for certain use cases.

## Design

SageMaker runtime endpoint expects predictions available at /invocations and a /ping status which is not provided by SCR server. So, the solution includes building a new “REST API server” that forwards/routes requests from SageMaker to SCR Server. Basically, this new server acts as a proxy to the SCR server for routing requests from SageMaker and we will call it as “sagemaker proxy” henceforth. We included this proxy in the new OCI image we created.

SAS scoring server(tomcat server) by default writes to /tmp which is not permitted in SageMaker docker “secured” containers and so we provide override to that in new OCI image.

Also, we need to change default port (8080) used by SAS REST API server since 8080 is used by “sagemaker proxy” we built.


## Implementation Details

The solution “tool kit” involves a little bit of following:
- Dockerfile – to create a new docker image using SCR OCI as base
- Python Flask framework – To create a new proxy for routing requests
- AWS SageMaker SDK – To create SageMaker assets for inference.

iPython notebook SCR_ModelOps_on_sagemaker.ipynb provides a documented walk-thru of solution along with pre-requisites


#### Code notes

- Python libraries used – Python Flask and AWS SageMaker SDK
- To keep notebook idempotent there are two variables in code snippets that get updated thru “Unix sed”. The two files in question are Dockerfile and sagemaker_server.py and variables are SCR_IMAGE_PATH and SCR_MODEL_NAME. Please watch variables are updated properly. If docker image build fails pay attention to those two file updates through “sed commands”
- Please note SCR REST API server uses 9090 port and the new “SageMaker proxy server” uses port 8080 to meet AWS requirements.
- Also, the two REST API servers are launched through script launch_two_servers.sh. I used popular WSGI “gunicorn” server to keep up performance.
- Python Flask app (sagemaker_server.py) initially tried to address /invocations by doing a redirect (HTTP 302) to SCR server but that failed since “sagamaker runtime” could not handle redirects (unlike a curl –location which can follow redirects). So, I customized “sagemaker_proxy” server to act as both HTTPClient and HTTP Server. It is a HTTPCleint making requests to SCR REST API server and HTTP Server for SageMaker to call it.
- While this new “sagemaker proxy” may add an extra hop it does not affect performance by margin since routing happens locally with in the container pod. See “localhost” reference in sagemaker_server.py. So, all traffic is limited to within the pod.
