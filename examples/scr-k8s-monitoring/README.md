# Configuring Monitoring for SAS Container Runtime on Kubernetes

This README describes how to configure monitoring using Helm for a SAS Container Runtime container that is deployed using Kubernetes.

## Prerequisites

The following applications must be installed on the host system where the SAS Container Runtime containers will be deployed:

* Kubernetes Cluster
* Helm

## Configuration and Usage

Edit the sas-container-runtime.yaml file to specify the number of pods, the SAS Container Runtime image file, resource limit specifications, and the desired environment variables.

For information about how to configure SAS Container Runtime, see the
 [SAS Container Runtime documentation](https://documentation.sas.com/?cdcId=mascrtcdc&cdcVersion=default).

The Prometheus configuration in the file enables Prometheus to automatically discover the SAS Container Runtime pods.

You can deploy SAS Container Runtime and the Ingress rules together as follows:

```bash
kubectl apply -f sas-container-runtime.yaml -f nginx-ingress.yaml
```

You can install multiple Helm charts to monitor SAS Container Runtime. You configure Helm charts by overriding assigned chart values. For more information, see the Helm documentation.

Here is an example that shows the commands that add some common chart repositories, and then installs them.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add fluent https://fluent.github.io/helm-charts
helm repo add elastic https://helm.elastic.co
helm repo add nginx-stable https://helm.nginx.com/stable
helm repo update
  
helm install -f values/prometheus.yaml prometheus prometheus-community/prometheus
helm install -f values/grafana.yaml grafana grafana/grafana
helm install -f values/fluentd.yaml fluentd fluent/fluentd
helm install elasticsearch elastic/elasticsearch
helm install kibana elastic/kibana
helm install nginx nginx-stable/nginx-ingress
```

By default, the Ingress rules specify the following:

* the Grafana dashboard is accessible at <http://grafana.localhost>.
* the Kibana dashboard is accessible at <http://kibana.localhost>.

To obtain the default password for the Grafana `admin` account, you can run this command:

```bash
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

To work with Elasticsearch data, you must first create a Kibana index pattern. For more information, see the Kibana documentation.

## Additional Resources

Here are some locations where you can obtain more information about some common Helm charts and their values:

* [Prometheus](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus)
* [Fluentd](https://github.com/fluent/helm-charts/tree/main/charts/fluentd)
* [Grafana](https://github.com/grafana/helm-charts/tree/main/charts/grafana)
* [Elasticsearch](https://github.com/elastic/helm-charts)
* [Kibana](https://github.com/elastic/helm-charts/tree/main/kibana)
* [Nginx](https://github.com/kubernetes/ingress-nginx/tree/main/charts/ingress-nginx)
