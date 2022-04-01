import yaml
import os.path
from kubernetes import client, config, utils
      
#############################################################################################
# Following prints a list of all SAS models both active/running and inactive/ready_for_scoring
# 
def list_knative_models(kubeconfig_path,k8s_namespace, knative_scoring_ingress_host):
    list_nodes, list_pods, list_ksvcs = True, True, True
    try:
        if os.path.exists(kubeconfig_path):
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            print("kubeconfig file not found")
            return
     
        v1 = client.CoreV1Api()
     
        if list_nodes:
            print("=============================================================")
            print("List of nodes in cluster: ")
            res = v1.list_node()
            #print("result type: ", type(res), type(res.items))
            for i in res.items:
                print(i.metadata.name, i.status.conditions[-1].type)
    
        if list_pods:
            print("======================")
            print("List of Running pods/Active models scoring currently in cluster: ")
            res = v1.list_namespaced_pod(namespace=k8s_namespace)
            #print("result type: ", type(res), type(res.items))
            for i in res.items:
                print(i.metadata.name, i.status.phase)
     
        if list_ksvcs:
            print("======================")
            print("List of knative svcs/Ready models for scoring in cluster: ")
            print("Model Name, Model deployed date, Model Generation and Container Image Path and ScoringURL")
            api = client.CustomObjectsApi()
            res = api.list_namespaced_custom_object(group="serving.knative.dev",
                version="v1",
                plural="services",
                namespace=k8s_namespace)
            #print("result type: ", type(res), type(res['items']))
    
            for i in res['items']:
                #print("i", i)
                if i['status']['conditions'][0]['status'] == 'True':
                    print(i['metadata']['name'], ",", i['metadata']['creationTimestamp'],",", i['metadata']['generation'],",",i['spec']['template']['spec']['containers'][0]['image'],",", "ScoringURL", knative_scoring_ingress_host+i['metadata']['name']+"/")
                else:
                    print(i['metadata']['name'], ",", i['metadata']['creationTimestamp'], ",",i['metadata']['generation'], ",",i['spec']['template']['spec']['containers'][0]['image'], ",", "Service not ready. Debug ksvc with k8s admin if issue persists more than 5-10 min")
            
            print("===============================================================") 
     
    except Exception as e:
        print(str(e))
        raise e
          
