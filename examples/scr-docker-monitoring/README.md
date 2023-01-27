# Configuring Monitoring for SAS Container Runtime on Docker

This README describes how to configure monitoring for a SAS Container Runtime container that is deployed using Docker.

## Prerequisites

The following applications must be installed on the host system where the SAS Container Runtime containers will be deployed:

* Docker
* Docker Compose

## Configuration and Usage

Edit the docker-compose.yaml file to specify the SAS Container Runtime image file and the desired environment variables.

For information about how to configure SAS Container Runtime, see the
 [SAS Container Runtime documentation](https://documentation.sas.com/?cdcId=mascrtcdc&cdcVersion=default).

When complete, run the following command to create and start the containers:

```bash
docker compose up -d
```

By default, the port forwarding rules specify the following:

* The Grafana dashboard is accessible at <http://localhost:3000>.
* The Kibana dashboard is accessible at <http://localhost:5601>.

The default login for Grafana is `admin` for both the user name and password.

To work with Elasticsearch data, you must first create a Kibana index pattern. For more information, see the Kibana documentation.
