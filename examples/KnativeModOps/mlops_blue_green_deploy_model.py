import os
from scr_utils import knative_8s_utils

KUBECONFIG_PATH="kube_config.yaml"
K8S_NAMESPACE="sas-model-inference"
KNATIVE_SCORING_INGRESS_HOST="http://12.12.12.12"
KNATIVE_SCORING_INGRESS_HOSTNAME="ingress.company.com"

# model we are dealing fpr this run
model_name = "creditwriteoff"
model_timeout= "600s"

if __name__ == "__main__":

    # step1 List all revisions out there for a given model
    knative_8s_utils.list_knative_revisions(KUBECONFIG_PATH,K8S_NAMESPACE,KNATIVE_SCORING_INGRESS_HOST,model_name)

    # step 2. Deploy a new revision for an existing model
    # revision name should have model_name has prefix else it fails to deploy a new revision
    # blue is the old revision name u get from list_knative_revisions.
    blue_revision_name = "creditwriteoff-p5l52"
    blue_percent = 75

    green_revision_name="creditwriteoff-50"
    green_percent = 25
    green_revision_imagepath= "dockerrepo.company.com:5003/creditwriteoff:5.0"
    #knative_8s_utils.deploy_revision_to_knative(KUBECONFIG_PATH,K8S_NAMESPACE, model_name, blue_revision_name, blue_percent, green_revision_name, green_percent, green_revision_imagepath,model_timeout)

    # Step3. See updated revisions
    #knative_8s_utils.list_knative_revisions(KUBECONFIG_PATH, K8S_NAMESPACE, KNATIVE_SCORING_INGRESS_HOST, model_name)

    # Step4 . Flip versions
    # Flip Blue/Green where we change traffic percentages. We make all traffic go to new one
    blue_revision_name = "creditwriteoff-p5152"
    blue_percent = 0
    green_revision_name = "creditwriteoff5.0"
    green_percent = 100
    #knative_8s_utils.deploy_revision_to_knative( KUBECONFIG_PATH,K8S_NAMESPACE, model_name, blue_revision_name, blue_percent, green_revision_name, green_percent, green_revision_imagepath,model_timeout)

    # Step5. see revisions again along with traffic
    #knative_8s_utils.list_knative_revisions(KUBECONFIG_PATH, K8S_NAMESPACE, KNATIVE_SCORING_INGRESS_HOST, model_name)

    # Step6. Delete old revision if we decide so. But delete works only after a revision traffic is set to 0. We can only delete blue whose traffic is set to 0.
    #knative_8s_utils.delete_revision_knative(KUBECONFIG_PATH,K8S_NAMESPACE, blue_revision_name)
