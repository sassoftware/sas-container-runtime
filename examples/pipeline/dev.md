# How to Develop with This Repository

- [Install](#install)
- [Setup](#setup)
- [Build the Images Specific to this Application](#build-the-images-specific-to-this-application)
- [Start the Services](#start-the-services)
- [Run the Application from a User Interface](#run-the-application-from-a-user-interface)
- [Obtain a Redis Viewer](#obtain-a-redis-viewer)
- [Running on Azure](#running-on-azure)
  - [Push the Images to Azure Container Registry](#push-the-images-to-azure-container-registry)
  - [Edit the docker-compose-azure.yml File](#edit-the-docker-compose-azureyml-file)
  - [Create Azure App Services](#create-azure-app-services)
- [Run the App](#run-the-app)
- [Run on a Kubernetes Cluster](#run-on-a-kubernetes-cluster)

## Install

Install the necessary packages:

```sh
npm install
```

At this point you have all the necessary js script packages.

## Setup

The example assumes that the SAS Container Runtime image has the name homeloan.

For convenience, a ZIP file of a homeloan model is included in the models directory. You can import that into SAS Model Manager and create your SAS Container Runtime image.

If you already have SAS Container Runtime models, you can use those instead. If you use your own models, the following changes must be made:

- Replace all references to hmeq.csv with the CSV file that is appropriate for your model.
- Replace all references to homeloan with the name of your SAS Container Runtime image.

Run the following command:

```bash
scripts/setup.sh
```

At this point, you have all the Docker images that are needed to run the application.

## Build the Images Specific to This Application

Issue this command in a bash shell:

```bash
./build.sh
```

## Start the Services

To start the services, run the following command:

```sh
docker compose up
```

## Run the Application from a User Interface

To run the application from a user interface, do the following:

1. Visit this site:  <http://localhost:8080/>

2. Enter values, and then click the **Run Pipeline** button.

The values are as follows:

Key - each output record in Redis has a key of the form: *key:recordno*.

Count - The number of records in hmeq.csv that you want to run.

Since the debug logging is on by default, you should avoid running too many records. If you want to run a lot of records, comment out the DEBUG environment variables in docker-compose file.

The application uses hmeq.csv as the data source.

When the run is complete, you can find the data for a given key.

## Obtain a Redis Viewer

There are a few free Redis viewers available, such as RedisInsight from Redis.

## Running on Azure

### Push the Images to Azure Container Registry

To push the images to Azure Container Registry, run the following command:

```sh
start/push.sh crname crhost
```

Here is an example:

```sh
start/push.sh mycr  mycr.azurecr.io
```

This moves all the images to your Azure container registry.

### Edit the docker-compose-azure.yml File

Apply a global change to the docker-compose-azure.yml file to apply your container registry information. For example, rename scrdemosrgcr.azurecr.io to mycr.azurecr.io.

When complete, save the file.

### Create Azure App Services

Use the Azure Portal to create a new Azure App.

In the Create window, do the following:

- Read and follow the instructions that are provided in the window.

- Make sure you select **Publish as Docker container**.

- Select your desired region and operating system (Linux is the typical choice).

- Select the **Next: Docker** button.

- In the second window, do the following:

    1. Under **Options** select **Docker Compose**.

    2. Select **Azure Container Registry for Image Source**.

    3. Select your registry.

    4. For **Configuration File**, point it to the docker-compose-azure.yml file in your project.

    5. Select **Review and Create the App Service**.

    6. When the service is created, set **WEBSITES_PORT** to *8080*.

        - Select **Configuration**.

        - Select **New Application Setting**.

        - Add WEBSITES_PORT as 8080.

        - Save the new values and, when prompted, accept the restart request.

## Run the App

In your browser enter the url from the Overview window. Replace https with *http*.

For example, if the app name is hlpipeline, you would enter the following:

<http://hlpipeline.azurewebsites.net/>

**Notes**:

- The first invocation might take some time.

- Since the Redis port cannot be exposed through Azure Apps, you cannot use the RedisInsight user interface.

## Run on a Kubernetes Cluster

1. Convert the docker-compose file to a deployment.yaml file using
 [kompose](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/).

2. Complete your process on the cluster.
