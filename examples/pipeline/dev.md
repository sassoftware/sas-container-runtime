# How to develop with this repository

## Install

Install the necessary packages.

```sh
npm install
```

At this point you will have all the necessary js script packages

## setup

The example assumes that the SCR image is named homeloan.
For convenience, a zip file of a homeloan model is included in the models directory. You can import that into SAS Model Manager and create your SCR image.

If you already have SCR models feel free to use those instead. If you choose to use your own, the following changes must be made:

- Replace all references to hmeq.csv with the csv file appropriate for your model.
- Replace all references to homeloan with the name of your SCR image.

```bash
scripts/setup.sh
```

At this point you have all the docker images needed to run the application

## Build the images specific to this application

Issue this command in a bash shell. If you are running cmd shell or power shell
./build.sh

## To start the services

docker compose up

## To run the application from an UI

Visit this site:  <http://localhost:8080/>

Enter values and press the Run Pipeline button.

The values are:

Key - each output record in redis will have a key of the form key:recordno

Count - how many of the records in hmeq csv you want to run.

Since the debug logging is on by default avoid running too many records. If you want to run a lot of them comment out the DEBUG environment variables in docker-compose file.

The application uses hmeq.csv as the data source.

Once the run is complete you can find the data for a given key.

## redisInsight viewer

There are a few free ones out there. I am using RedisInsight from Redis - but if you use it be prepared to get a call from their sales rep.

## Running on Azure

### Push the images to azure cr

```sh
start/push.sh crname crhost

ex: start/push.sh mycr  mycr.azurecr.io
```

This will move all the images to your azure cr

### Edit docker-compose-azure.yml

Do a global change:

Example:

scrdemosrgcr.azurecr.io to mycr.azurecr.io

Do not forget to save the file.

### Create a Azure App Services

Use the Azure portal and create a new Azure App
In the create dialog:

- follow the instructions in the window.

- Make sure you select 'Publish" as Docker container

- Select your desired region and operating system( Linux is our usual choice)

- Select the Next: Dockre button

- In this second window you will do the following:

    1. Under Options select Docker Compose

    2. Select Azure Container Registry for Image Source

    3. Select your registry

    4. For configuration file point it to the docker-compose-azure.yml in your project.

    5. Review and Create the App Service.

    6. Once the service is created you need to set WEBSITES_PORT to 8080

        - Select configuration

        - Select New Applicatioon Setting.

        - add WEBSITES_PORT as 8080

        - Save the new values and accept the restart request.

## Running the app

In your browser enter the url from the Overview window. Replace https with http.
For example, my appname is hlpipeline.
I enter <http://hlpipeline.azurewebsites.net/>

I have noticed that the first invocaton might take time. You just have to be patient. Once it is up you are good to go.

> Since the redis port cannot be exposed thru Azure Apps, you cannot use the redisInsight UI. I think it can be done by setting up a front door. I will leave that as an exercise for the reader.

## Running on a K8s cluster

1. Convert the docker-compose file to a deployment. yaml file using
 [kompose](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/)

2. Then do your thing on the cluster.

> Warning: I have not done this step for this app(but have used kompose before) - so leaving this as an exercise for the reader.
