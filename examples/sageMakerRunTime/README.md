# SAS Container Runtime - SAS Model Scoring on AWS SageMaker

- [Overview](#overview)
- [Motivation for Using SageMaker Runtime](#motivation-for-using-sagemaker-runtime)
- [Design](#design)
- [Implementation Details](#implementation-details)
- [Code Notes](#code-notes)

## Overview

AWS SageMaker Hosting services provides a runtime environment for custom model containers. Customers who are looking for guidance can follow the approach in this document to deploy SAS models to SageMaker Hosting services. SAS Container Runtime models need a few adjustments before they can run on AWS SageMaker.

## Motivation for Using SageMaker Runtime

Customers who are currently using SageMaker for all runtime scoring might prefer to use it for SAS Container Runtime models. Moreover, SageMaker Hosting services provide auto-scaling and model invocation statistics that can be useful in certain use cases.

## Design

The SageMaker runtime endpoint expects predictions at /invocations and a /ping status to be available. These are not provided by the SAS Container Runtime server. Therefore, this solution includes building a new REST API server that forwards requests from SageMaker to the SAS Container Runtime server. Basically, this new server acts as a proxy to the SAS Container Runtime server to route requests from SageMaker. This document refers to that as *sagemaker proxy*. This proxy is included in the new Open Container Initiative (OCI) image that is created.

The SAS scoring server (Tomcat server) writes to /tmp by default. This is not permitted in SageMaker Docker secured containers. Therefore, an override to that is provided in new OCI image.

Also, the default port (8080) that is used by the SAS REST API server must be changed since 8080 is used by the SageMaker proxy.

## Implementation Details

The solution toolkit involves some of each of the following:

- Dockerfile – Used to create a new Docker image using SAS Container Runtime as a base.
- Python Flask framework – Used to create a new proxy for routing requests.
- AWS SageMaker SDK – Used to create SageMaker assets for inference.

The Jupyter notebook SCR_ModelOps_on_sagemaker.ipynb provides a documented walk-through of a solution, including prerequisite information.

## Code Notes

- Here are the Python libraries that are used:
  - Python Flask
  - AWS SageMaker SDK

- To keep the notebook idempotent, there are two variables in code snippets that are updated through UNIX sed. These files are as follows:

  - Dockerfile
  - sagemaker_server.py

  The variables are SCR_IMAGE_PATH and SCR_MODEL_NAME. Confirm that the variables are updated properly. If the Docker image build fails, pay attention to those two file updates through UNIX sed commands.
  
- Note that the SAS Container Runtime REST API server uses port 9090 and the new SageMaker proxy server uses port 8080 (to meet AWS requirements).

  The two REST API servers are launched through the launch_two_servers script.sh. You can consider using the Web Server Gateway Interface (WSGI) gunicorn server help performance.

- The Python Flask app (sagemaker_server.py) initially tries to address /invocations by doing a redirect (HTTP 302) to the SAS Container Runtime server, but that fails because SageMaker Runtime could not handle redirects (unlike a curl –location, which can follow redirects).

  You can customize the sagemaker_proxy server to act as both HTTPClient and HTTP Server. HTTPCleint makes requests to the SAS Container Runtime REST API server and the HTTP Server for SageMaker calls it.

- This new SageMaker proxy adds an extra hop, but it does not affect performance by margin. This is because routing happens locally within the container pod. See the localhost reference in sagemaker_server.py. All traffic is limited to the pod.
