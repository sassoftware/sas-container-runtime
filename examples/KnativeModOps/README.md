# Automate Scalable Inference Setup Using Knative Kubernetes

- [Overview](#overview)
- [Motivation for Automation](#motivation-for-automation)
- [Knative KSVC](#knative-ksvc)
- [Implementation Details](#implementation-details)

## Overview

Using SAS Container Runtime, models can be published to any container registry. A customer can decide how to launch (deploy) a container runtime for scoring or inference. Customers looking for guidance can use the following approach to deploy models, and then be ready for scoring.

## Motivation for Automation

The typical data scientist focuses on model development, training, validation, and scoring. The setup of SAS Container Runtime scoring requires some knowledge of Kubernetes, Ingress, networking, storage, etc. Data scientists who do not have that knowledge, typically need to work with a Kubernetes administrator or a Machine Learning platform engineer.

Similarly, when a new model is created or an existing model needs to be updated, a data scientist often needs to contact a machine learning platform engineer for assistance. The guidance in this document might help to avoid the necessity for that assistance.

The objective here is to provide a "Python toolkit" that a data scientist can use to manage Machine Learning Ops (MLOps) for SAS Container Runtime models. That is, to set up and manage a robust and scalable inference environment. The “Python toolkit” is intended to be a complete automated solution that can:

- Create necessary the container runtime instances without manual operations.

- List all available model containers that are currently running and delete model container runtime instances.

- Score given an input CSV file (with column headings) and model name.

## Knative KSVC

This example uses Knative ksvc as an abstraction for each model to be deployed to a Kubernetes cluster.

- **Elastic Inference** - Provides automated scalable inference out of the box by scaling pods on Kubernetes to provide inference as REST API services.

- **Scale to Zero** - Scales to zero pods if there are no input requests.

- **A/B model scenarios** - Provides the means to set up A/B model scoring using "knative revisions" and "traffic percentage" constructs.

## Implementation Details

### Prerequisites

- Knative must be installed and configured. See <https://knative.dev/docs/install> for more information.
  
- Full “namespace” permissions are required to create deployment objects, Ingress, etc. on a namespace that is dedicated for model inference.  (It is called  “sas-model-inference” in this implementation). A “kube-config.yaml” that reflects those permissions is required.

- A Python environment with the Kubernetes package and typical REST API support packages (such as request, urllib, etc.) are installed.
  
- PROC Python is configured to support the Python environment needs cited above. This is needed only if managing SAS Container Runtime model ops from SAS Studio. SAS Container Runtime model ops can also be managed using a regular Python environment (jupyterhub, etc.). In that case, the work is done outside of SAS Studio.

- You have access to a private Docker destination or any container registry (that contains published SAS Container Runtime model images). To access secure container registries using Knative:
  
  1. Create a secret: kubectl create secret docker-registry *registry-credential-secrets*.
  2. Patch the default account in sas-model-inference: kubectl patch serviceaccount default -p "{\"imagePullSecrets\": [{\"*name*\": \"*container-registry*\"}]}"

- All the models that you plan to manage are published to the container registry.

### Process Overview for a Data Scientist

1. Work with your Kubernetes and SAS Viya platform administrators to complete the prerequisites.
2. Git clone code from <https://github.com/sassoftware/sas-container-runtime>.
3. Access the KNativeModOps folder.
4. Copy kube-config.yaml to the location root directory of the above code.
5. If PROC PYTHON is set up, then the SAS Container Runtime model ops can be completed using SAS Studio and the mlops_scr_model.SAS file. The code is self-explanatory. You can assign variable names to replace model_name, model_imagepath, etc.
6. You can list all models that are currently available for scoring.

   - Create a new knative service – essentially, this deploys a model to a Kubernetes system for scoring.
  
   - Delete a knative service – this removes the model container runtime.
  
7. If PROC PYTHON is not set up, use mlops_scr_model.py and follow the same operations as mentioned in the previous step.
8. For scoring, use the score_csv_with_scr.* files for guidance. Specify the variables in the file.

### Code Notes

- Python libraries – Python Kubernetes API (obtain the latest), request, urllib3, and the typical standard libraries are used.
- Knative Service - A Kubernetes API custom object Knative Service represents a SAS Container Runtime model runtime on Kubernetes. Each SAS Container Runtime model is represented by a Knative service. Once created, the Knative Service offers a SAS Container Runtime scoring REST API service to external clients.
- Model and Knative Management – The /scr_utils/knative_8s_utils.py file provides methods to list, create, and delete Knative custom objects to meet the requirements. This needs kube_config.yaml permissions for handling Kubernetes object management.
- Scoring component – The scr_utils/score_utils.py file uses request and urllib methods to make REST API calls. This does not need a kube_config.yaml file or Kubernetes permissions. Any client with URL information can access a model’s REST API call for scoring.
