import yaml
import os.path
from kubernetes import client, config, utils
      
###########################################################################################################
#### Following deploys a knative service
##
def deploy_model_to_knative(kubeconfig_path, k8s_namespace, knative_scoring_ingress_host, knative_scoring_ingress_hostname, model_name, model_imagepath,model_timeout):
     
    import re
      
    sas_model_knative = {
       "apiVersion": "serving.knative.dev/v1",
       "kind": "Service",
       "metadata" : {
            "name": model_name,
        },
       "spec": {
            "template": {
               "metadata": {
                 "annotations": {
                     "autoscaling.knative.dev/window": model_timeout
                 }
               },
               "spec": {
                 "containers": [{
                    "image": model_imagepath,
                  }]
                }
            }
       }
    }
      
    if not re.match("^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$",model_name):
        print(model_name, "name should not have underscores etc and should match to a DNS Label convention")
        return
      
    try:
        if os.path.exists(kubeconfig_path):
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            print("kubeconfig file not found")
            return
      
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        api = client.CustomObjectsApi()
     
        resource = api.create_namespaced_custom_object(
                group="serving.knative.dev",
                version="v1",
                plural="services",
                namespace=k8s_namespace,
                body=sas_model_knative)
    
        print("model deployed successfully. Can be inferenced at ",knative_scoring_ingress_host+model_imagepath.split('/')[-1])
        print("Since are using load balancer we need to put in Host in header info like this: ","-HHost:"+model_name+"."+k8s_namespace+"."+knative_scoring_ingress_hostname )
     
    except Exception as e:
       print(str(e))
       raise e
     
