# SCR - Automate scalable inference setup using Knative/K8S

<blockquote>
With Viya4 SAS Container Runtime(SCR) models can be published to any container registry.  SAS/Viya4 lets customer decide on how to launch(deploy) a container runtime for scoring or inference. Customers looking for guidance can follow undermentioned approach to deploy models and be ready for scoring.

</blockquote>

## Motivation for Automation

Typical Data scientist focus is on model development, training, validation and scoring. Setting up SCR scoring requires some knowledge of Kubernetes, Ingress, networking, storage etc. Data scientists may not be familiar with those areas and may need to approach a Kubernetes/ML platform engineer. Every time a new model is created or a current model is updated he/she needs to reach to ML platform engineer for setting this up. We think it should not be the case.

Objective is to provide a “python toolkit” that a Data scientist can use to manage ML Ops for SCR models, that is to setup and manage a robust /scalable inference environment. The “python toolkit” is intended to be a complete automated solution that can:

- Create necessary container run time instances without manual operations. Additionally, list all available model containers currently running and delete model container runtime instances.
Score given an input csv file and a “model name”.

- Score given an input CSV file (with column headers) and model name.

## Knative KSVC

This example choose Knative KSVC as an abstraction for each model to be deployed to K8S cluster for undermentioned reasons.

- `Elastic Inference` - Knative provides automated scalable inference out of box by scaling number of pods on k8s to provide inference as REST API services.

- `Scale to Zero` - Scales to zero pods if there are no input requests.

- `A/B model scenarious` - Provides means to setup A/B model scoring using 'knative revisions" and "traffic percentage" constructs.

## Implementation Details

#### Pre-requisites

1. Knative setup – https://knative.dev/docs/install/any-kubernetes-cluster/
2. Full “namespace” permissions to create deployment objects, ingress etc on a namespace dedicated for model inference (we called it as “sas-model-inference” in this implementation). Basically, we need a “kube-config.yaml” reflecting those permissions.
3. Python environment with “Kubernetes” package installed along with typical REST API support packages like “request, urllib etc”.
4. PROC python configured to support above python environment needs. We need this only if we were to manage “SCR model ops” from SASStudio. We can also manage SCR model ops using regular python environment (jupyterhub etc) in which case we will working on this outside SASStudio.
5. Access to a private docker destination or any container registry (holding published SCR model images). One way to access secure container registries from knative:
Create a secret $k create secret docker-registry …
Patch default account in “sas-model-inference” using $k patch serviceaccount default -p ‘{\”imagePullSecrets\”: …
6. Assumes all models you plan to manage are published at this point to container registry.


#### User Guide(sort of for Data scientist)

1. Work with Kubernetes/viya4 administrator to get the pre-requisites covered.
2. Git clone code from https://github.com/sassoftware/sas-container-runtime
3. Get to KNativeModOps for this specific example.
4. Copy “kube-config.yaml” to location root directory of above code where it can access.
5. If proc python is setup, then SCR model ops can be done using SASStudio and mlops_scr_model.sas file. Code is self-explanatory you can put in variables names to cover settings such as model_name, model_imagepath etc
6. You can list all models currently available for scoring
  - Create a new knative service – basically deploy a model to k8s system for scoring
  - Delete a knative service – remove the model container runtime
7. If proc python is not setup, then use mlops_scr_model.py and follow the same operations as mentioned in prior step
8. Scoring – score_csv_with_scr.sas/py files help with scoring aspect. Provide the variables


#### Code notes

- Python libraries used – python Kubernetes API (get latest), request, urllib3 and usual standard libraries.
- Kubernetes API custom object “knative services” represent one-to-one “SCR model container runtime” on K8S. Each SCR model is represented by a “Knative service”. Once created, knative service offers “SCR scoring REST API” service to external clients.
- Model/Knative Management – “scr_utils/knative_8s_utils.py” provides methods to list/create/delete knative custom objects to meet our requirements. This does need “kube_config.yaml” permissions which it loads for handling Kubernetes object management.
- Scoring component – scr_utils/score_utils.py uses request, urllib methods to make REST API calls. This does not need any “kube_config.yaml” or Kubernetes permissions. Any client with URL information can access model’s RESTAPI call for scoring.
