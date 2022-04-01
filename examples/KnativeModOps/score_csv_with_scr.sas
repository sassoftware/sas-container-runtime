
%let K8S_NAMESPACE=sas-model-inference;
%let KUBECONFIG_PATH=/xxxx/home/scr-knative-model-lifecycle/kube_config.yaml;
%let KNATIVE_SCORING_INGRESS_HOST=12.12.12.12 ;
%let KNATIVE_SCORING_INGRESS_HOSTNAME=ingress.company.com ;

%let MODEL_NAME=decision-tree-pipeline-3-0 ;
%let CONTAINER_IMAGE_NAME=decision_tree__pipeline_3_0 ;

%let MODEL_NAME=sr-hmeq-logreg ;
%let CONTAINER_IMAGE_NAME=sr_hmeq_logreg ;

%let SCORE_INPUT_FILE=/sgrid/home/sunall/groot/scr-knative-model-lifecycle/credit_writeoff_score_input.csv ;
%let SCORE_OUT_FILE=/sgrid/home/sunall/groot/scr-knative-model-lifecycle/credit_writeoff_score_output.csv ;
%let SCORE_INPUT_FILE=/sgrid/home/sunall/groot/scr-knative-model-lifecycle/hmeq.csv ;
%let SCORE_OUT_FILE=/sgrid/home/sunall/groot/scr-knative-model-lifecycle/hmeq_output.csv ;

filename p_score '/sgrid/home/sunall/groot/scr-knative-model-lifecycle/scr_utils/score_utils.py';


/****************************************************************************************
SCORE model using CSV file as input
******/
proc python infile=p_score TERMINATE ;
submit;
K8S_NAMESPACE=SAS.symget('K8S_NAMESPACE')
KUBECONFIG_PATH=SAS.symget('KUBECONFIG_PATH')
KNATIVE_SCORING_INGRESS_HOST=SAS.symget('KNATIVE_SCORING_INGRESS_HOST')
KNATIVE_SCORING_INGRESS_HOSTNAME=SAS.symget('KNATIVE_SCORING_INGRESS_HOSTNAME')
MODEL_NAME=SAS.symget('MODEL_NAME')
CONTAINER_IMAGE_NAME=SAS.symget('CONTAINER_IMAGE_NAME')
SCORE_INPUT_FILE=SAS.symget('SCORE_INPUT_FILE')
SCORE_OUT_FILE=SAS.symget('SCORE_OUT_FILE')
print("#################  Python output #################### ")
score_input_file(K8S_NAMESPACE, KNATIVE_SCORING_INGRESS_HOST,KNATIVE_SCORING_INGRESS_HOSTNAME,MODEL_NAME,CONTAINER_IMAGE_NAME,SCORE_INPUT_FILE, SCORE_OUT_FILE)
endsubmit;
run;
