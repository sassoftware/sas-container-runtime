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
            print("======================")
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
                    print(i['metadata']['name'], ",", i['metadata']['creationTimestamp'],",", i['metadata']['generation'],",",
                        i['spec']['template']['spec']['containers'][0]['image'],",", "ScoringURL", knative_scoring_ingress_host+i['metadata']['name']+"/")
                else:
                    print(i['metadata']['name'], ",", i['metadata']['creationTimestamp'], ",",
                          i['metadata']['generation'], ",",
                          i['spec']['template']['spec']['containers'][0]['image'], ",", "Service not ready. Debug ksvc with k8s admin if issue persists more than 5-10 min")

    except Exception as e:
        print(str(e))
        raise e

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

##################################################################################################
############################################################################################
####################

# Following prints a list of all revisions for a given model
#
def list_knative_revisions(kubeconfig_path,k8s_namespace, knative_scoring_ingress_host, model_name):

    try:
        if os.path.exists(kubeconfig_path):
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            print("kubeconfig file not found")
            return

        v1 = client.CoreV1Api()

        print("======================")
        print("List of revisions for model: ", model_name)
        print("Model Revision, Ready, Generation, Container Image Path")
        api = client.CustomObjectsApi()
        res = api.list_namespaced_custom_object(group="serving.knative.dev",
               version="v1",
               plural="revisions",
               namespace=k8s_namespace)
        for i in res['items']:
            if i['metadata']['labels']['serving.knative.dev/configuration'] == model_name:
                #print("i: ", i)
                print(i['metadata']['name'],",", i['status']['conditions'][-1]['status'], ",", i['metadata']['labels']['serving.knative.dev/configurationGeneration'],
                      ",", i['spec']['containers'][0]['image'] )

        print("======================")
        print("Split of traffic by revision")
        res = api.list_namespaced_custom_object(group="serving.knative.dev",
                                                version="v1",
                                                plural="services",
                                                namespace=k8s_namespace)

        for i in res['items']:
            if i['metadata']['name'] == model_name:
                traffic_list = i['spec']['traffic']
                for traffic in traffic_list:
                    print("traffic: ", traffic)
                    #if traffic['revisionName']:
                    #    print(traffic['revisionName'],",",traffic['percent'],",",traffic['tag'])
                    #else:
                    #    print("traffic: ", traffic)

    except Exception as e:
        print(str(e))
        raise e


##
def deploy_revision_to_knative(kubeconfig_path, k8s_namespace, model_name, blue_revision_name, blue_percent, green_revision_name, green_percent, green_revision_imagepath, model_timeout):

    import re

    sas_revision_knative = {
       "apiVersion": "serving.knative.dev/v1",
       "kind": "Service",
       "metadata" : {
            "name": model_name,
        },
       "spec": {
            "template": {
               "metadata": {
                 "name": green_revision_name,
                 "annotations": {
                     "autoscaling.knative.dev/window": model_timeout
                 }
               },
               "spec": {
                 "containers": [{
                    "image": green_revision_imagepath,
                  }]
                }
            },
           "traffic": [
               {
                "tag": "blue",
                "revisionName": blue_revision_name,
                "percent": blue_percent
               },
               {
                   "tag": "green",
                   "revisionName": green_revision_name,
                   "percent": green_percent
               }
           ]

       }
    }


    if not re.match("^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$",model_name):
        print(green_revision_name, "name should not have underscores etc and should match to a DNS Label convention")
        return

    if not model_name in green_revision_name:
        print("revision name ",green_revision_name,"should have prefix of model name ", model_name)
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

        resource = api.patch_namespaced_custom_object(
                group="serving.knative.dev",
                version="v1",
                plural="services",
                name=model_name,
                namespace=k8s_namespace,
                body=sas_revision_knative)

        print("Revision deployed. All revisions reflect same model and URL REST API do not change")


    except Exception as e:
       print(str(e))
       raise e

# Delete the SAS model revision from knative setup..
def delete_revision_knative(kubeconfig_path, k8s_namespace, blue_revision_name):

    try:
        config.load_kube_config(config_file=kubeconfig_path)
        v1 = client.CoreV1Api()
        api = client.CustomObjectsApi()

        resource = api.delete_namespaced_custom_object(
                group="serving.knative.dev",
                version="v1",
                name = blue_revision_name,
                plural="revisions",
                namespace=k8s_namespace,
                body=client.V1DeleteOptions())
        print(blue_revision_name," Revision deleted from kubernetes/knative.")

    except Exception as e:
       print(str(e))
       raise e