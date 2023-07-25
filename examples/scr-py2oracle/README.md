# Information about Accessing Oracle in SAS Container Runtime via Python

This README contains information and instructions about how to access an Oracle database in SAS Container Runtime via a Python module. Here are the tasks:

- [Obtain and Configure the Required Python Package](#obtain-and-configure-the-required-python-package)
- [Add the Required Items to the Dockerfile](#add-the-required-items-to-the-dockerfile)
- [Review Sample Python Package Code](#review-sample-python-package-code)
- [Build and Start a SAS Container Runtime Container](#build-and-start-a-sas-container-runtime-container)
- [Execute the Python Package Calling Oracle](#execute-the-python-package-calling-oracle)
- [Access Oracle via Python without SAS Container Runtime](#access-oracle-via-python-without-sas-container-runtime)

---

## Obtain and Configure the Required Python Package

You must add the oracledb Python package to your requirements.txt file in order to pick up the Oracle library.

An example requirements.txt file is located in this project.

## Add the requirements.txt location to the Dockerfile

Here is a Dockerfile sample that shows the Python configuration and installation of the requirements.txt file:

```sh
USER root
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt 
```

An example Dockerfile file is located in this project.

## Review Sample Python Package Code

In the project there are two examples of Python package code that perform queries against an Oracle database (py2oracle_insert_module.json and py2oracle_select_module.json). The following lines will need to be modified to use your database information and credentials.

```sh
user='xyz',\n        password='xyz',\n        dsn='<server>:<port>/<path>'
```

## Build and Start a SAS Container Runtime Container

Create a base directory to copy the project files into. Create a subdirectory called modules. Place a single json file of the module you wish to use here. The rest of the files can be located in the base directory.

Use these commands to build and start the container from the base directory:

```sh
docker compose build
docker compose up
```

## Execute the Python Package Calling Oracle


Submit the following JSON payload to SAS Container Runtime to execute the module. (Here is a sample endpoint: http://localhost:8080/execute/execute)

```sh
{
"inputs": [
      {
        "name": "in_int",
        "value": 1
        }
]
}
```

Here is a sample response:

```sh
{
   "metadata" : {
      "module_id" : "execute",
      "elapsed_nanos" : 269232100,
      "step_id" : "execute",
      "timestamp" : "2023-07-25T18:59:33.332877700Z"
   },
   "version" : 1,
   "outputs" : [
      {
         "name" : "out_string",
         "value" : "test"
      }
   ]
}
```

## Access Oracle via Python without SAS Container Runtime

An example Python program to access Oracle without the use of SCR (py2oracle.py) is located in this project. Your database connection info and credntials will need to be filled in. This is useful to test the connection to your database before creating the SCR instance.
