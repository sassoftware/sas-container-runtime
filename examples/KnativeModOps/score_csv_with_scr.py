import os
from scr_utils import score_utils

K8S_NAMESPACE="sas-model-inference"
KNATIVE_SCORING_INGRESS_HOST="12.12.12.12"
KNATIVE_SCORING_INGRESS_HOSTNAME="ingress.company.com"
# model_name could be different from container image name. So provided two variables to cover the scope
# model name should match DNS website name standards and no underscore.

model_name = "sr-hmeq-logreg"
container_image_name = "sr_hmeq_logreg"
SCORE_INPUT_FILE="hmeq.csv"
SCORE_OUT_FILE="hmeq_output.csv"

model_name = "creditwriteoff"
container_image_name = "creditwriteoff"
SCORE_INPUT_FILE="credit_writeoff_score_input.csv"
SCORE_OUT_FILE="credit_writeoff_score_output.csv"


if __name__ == "__main__":

    score_utils.score_input_file(K8S_NAMESPACE, KNATIVE_SCORING_INGRESS_HOST,KNATIVE_SCORING_INGRESS_HOSTNAME, model_name, container_image_name, SCORE_INPUT_FILE, SCORE_OUT_FILE)
    print("Input file used for scoring: ", SCORE_INPUT_FILE)
    print("Output file used for scoring: ", SCORE_OUT_FILE)
