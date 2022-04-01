import os
from scr_utils import knative_8s_utils

KUBECONFIG_PATH="kube_config.yaml"
K8S_NAMESPACE="sas-model-inference"
KNATIVE_SCORING_INGRESS_HOST="http://12.12.12.12"
KNATIVE_SCORING_INGRESS_HOSTNAME="ingress.company.com"


if __name__ == "__main__":

    # List all models out there
    knative_8s_utils.list_knative_models(KUBECONFIG_PATH,K8S_NAMESPACE,KNATIVE_SCORING_INGRESS_HOST)

    # Deploy a new model to K8S/Knative env
    # keep modelname without underscores/dashes and names. Basically when you publish a model from ModelManager get rid of underscores and dashes as
    # istio and others which buluild ingresss DNS names will not permit underscores.
    # keep modelname(published name from modelmanager) consistent throughout the lifecycle of model as future revisions still use same modelname.
    model_name= "creditwriteoff"
    model_imagepath= "dockerrepo.company.com:5003/creditwriteoff:4.0"
    #model_name = "sr-hmeq-logreg"
    #model_imagepath = "fsbuviya4aksacr.azurecr.io/sr_hmeq_logreg"
    model_timeout= "600s"
    #knative_8s_utils.deploy_model_to_knative( KUBECONFIG_PATH,K8S_NAMESPACE,KNATIVE_SCORING_INGRESS_HOST, KNATIVE_SCORING_INGRESS_HOSTNAME, model_name, model_imagepath,model_timeout)

    # Delete the model.
    #knative_8s_utils.delete_model_knative(KUBECONFIG_PATH,K8S_NAMESPACE,model_name)
