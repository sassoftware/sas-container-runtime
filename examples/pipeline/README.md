# Pipeline: A Composition of Containers Including SAS Container Runtime

- [Introduction](#introduction)
- [Approach](#approach)
- [Basic Design - Multiple Container Deployment](#basic-design---multiple-container-deployment)
- [Batch Mode](#batch-mode)
- [Final Thoughts](#final-thoughts)

## Introduction

The repository explores a common SAS Container Runtime use case. This process is as follows:

1. Read data from a persisted source (for example, CSV files).
2. Score each of the records (scenarios) using a SAS Container Runtime container.
3. Forward the results to another container for further processing or persistence.

![simple-scenario](./public/pipeline-scenario.png)

## Approach

A multi-container deployment is used to create the pipeline shown in the figure above. The deployment uses the following containers to create the pipeline shown below.

![pipeline-simple](./public/pipeline-simple.png)

- **pipeline** - This service acts as an entry point to process runtime input from the user, and then pass it on to the database service.

- **database** - This service reads a specified CSV file and sends the data to the scrwrapper service. The database service does not wait for a response from the scrwrapper service. For other data sources, modify this service to read from the new source.

- **scrwrapper** - This service takes the input from the database service, scores it using SAS Container Runtime service, and then sends the output to persist service. The SAS Container Runtime container is specified by using the SCR_URL environment variable.

- **scr** - This is SAS Container Runtime running as a service to score the data.

- **persist** - This service takes the input and sends it to Redis for persistence.

- **redis** - This is the Redis database service, which persists the results.

## Basic Design - Multiple Container Deployment

All flows are controlled via environment variables.A service can call other services using the service name as the host.

In this proof of concept example, there are services called db and scrwrapper. The code in the db service can access service in scrwrapper using code as follows. The target URL (in this case it is scrwrapper/scrwrapper) is specified in the environment variable.

```js
let config = {
    url: 'http://scrwrapper/scrwrapper',
    method: 'POST',
    data: data
};

let r = await axios(config);
... do something...

```

## Batch Mode

Unlike in SAS Micro Analytic Service, SAS Container Runtime can be used to score in batch.

A sample code to execute a pipeline is shown in scripts/pipeline.js. This code is very similar to what is in the index.html file.

**Note**: Pay special attention to the container that feeds scrwrapper. Ideally there are multiple feeders working in parallel to feed that data to scrwrapper. This, along with replication of the services, provides the best option to process data in batch.

## Final Thoughts

The pattern in this proof of concept can be used to create a variety of pipelines. Here are some examples:

- **Database service** - Change it to read from a database, take a feed from Kafka, SAS Event Stream Processing, or other streaming services.

- **Redis** - Change it to a cloud storage, pass the URL to a service that calls the SAS Viya platform to do analysis of the output data.

- Add other services - both SAS and other types of containers.
