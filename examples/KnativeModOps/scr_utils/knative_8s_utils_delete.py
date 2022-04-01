import yaml
import os.path
from kubernetes import client, config, utils
      
##########################################################
# Delete the SAS model from knative setup..
def delete_model_knative(kubeconfig_path, k8s_namespace, model_name):
    
    try:
        config.load_kube_config(config_file=kubeconfig_path)
        v1 = client.CoreV1Api()
        api = client.CustomObjectsApi()
    
        resource = api.delete_namespaced_custom_object(
                group="serving.knative.dev",
                version="v1",
                name = model_name,
                plural="services",
                namespace=k8s_namespace,
                body=client.V1DeleteOptions())
        print(model_name, "Model deleted from kubernetes/knative. Container Image is not aletered. You can always redeploy")
   
    except Exception as e:
       print(str(e))
       raise e
   
###################
   
