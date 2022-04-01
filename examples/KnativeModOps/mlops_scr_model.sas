
%let K8S_NAMESPACE=sas-model-inference;
%let KUBECONFIG_PATH=/xxxx/home/scr-knative-model-lifecycle/kube_config.yaml;
/* following ingress_host used only for display purposes. So included http . */
%let KNATIVE_SCORING_INGRESS_HOST=http://12.12.12.12 ;
%let KNATIVE_SCORING_INGRESS_HOSTNAME=ingress.company.com ;

%let MODEL_NAME=decision-tree-pipeline-3-0 ;
%let MODEL_IMAGEPATH=dockerrepo.company.com:5003/decision_tree__pipeline_3_0;
%let MODEL_TIMEOUT=600s ;

%let MODEL_NAME=sr-hmeq-logreg ;
%let MODEL_IMAGEPATH=xxxxaksacr.azurecr.io/sr_hmeq_logreg;
%let MODEL_TIMEOUT=600s ;

filename p_list '/sgrid/home/xxx/groot/scr-knative-model-lifecycle/scr_utils/knative_8s_utils_list.py';
filename p_create '/sgrid/home/xxx/groot/scr-knative-model-lifecycle/scr_utils/knative_8s_utils_create.py';
filename p_delete '/sgrid/home/xxxx/groot/scr-knative-model-lifecycle/scr_utils/knative_8s_utils_delete.py';

/****************************************************************************************
READ operation of CRUD
First try to list all available models on namespace - both deployed models as well active/running models
list_knative_models(KUBECONFIG_PATH,list_nodes=True,list_pods=True,list_ksvcs=True)
******/
proc python infile=p_list TERMINATE ;
submit;
K8S_NAMESPACE=SAS.symget('K8S_NAMESPACE')
KUBECONFIG_PATH=SAS.symget('KUBECONFIG_PATH')
KNATIVE_SCORING_INGRESS_HOST=SAS.symget('KNATIVE_SCORING_INGRESS_HOST')
print("#################  Python output #################### ")
list_knative_models(KUBECONFIG_PATH,K8S_NAMESPACE,KNATIVE_SCORING_INGRESS_HOST)
endsubmit;
run;


/*********************************************
Create Knative service for the model - basically deploys model to k8s/knative system.
******/
proc python infile=p_create TERMINATE ;
submit;
K8S_NAMESPACE=SAS.symget('K8S_NAMESPACE')
KUBECONFIG_PATH=SAS.symget('KUBECONFIG_PATH')
KNATIVE_SCORING_INGRESS_HOST=SAS.symget('KNATIVE_SCORING_INGRESS_HOST')
KNATIVE_SCORING_INGRESS_HOSTNAME=SAS.symget('KNATIVE_SCORING_INGRESS_HOSTNAME')
MODEL_NAME=SAS.symget('MODEL_NAME')
MODEL_IMAGEPATH=SAS.symget('MODEL_IMAGEPATH')
MODEL_TIMEOUT=SAS.symget('MODEL_TIMEOUT')
print("#################  Python output #################### ")
deploy_model_to_knative(KUBECONFIG_PATH,K8S_NAMESPACE,KNATIVE_SCORING_INGRESS_HOST, KNATIVE_SCORING_INGRESS_HOSTNAME,MODEL_NAME,MODEL_IMAGEPATH,MODEL_TIMEOUT)
endsubmit;
run;

/**************************************************
Delete model from knative system
****/
proc python infile=p_delete TERMINATE ;
submit;
K8S_NAMESPACE=SAS.symget('K8S_NAMESPACE')
KUBECONFIG_PATH=SAS.symget('KUBECONFIG_PATH')
MODEL_NAME=SAS.symget('MODEL_NAME')
print("#################  Python output #################### ")
delete_model_knative(KUBECONFIG_PATH,K8S_NAMESPACE,MODEL_NAME)
endsubmit;
run;

*/
