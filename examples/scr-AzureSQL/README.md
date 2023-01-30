# Accessing Azure SQL in SAS Container Runtime via Python

## Overview<a name="intro"></a>

This README contains information and instructions about how to access an Azure SQL database in SAS Container Runtime via a Python module. For more information about Azure, see the [Azure documentation](https://learn.microsoft.com/en-us/azure/azure-sql/database/connect-query-python?view=azuresql).

Here are the requirements and tasks that are involved in this process:

* [Prerequisites](#req)
* [SAS Intelligent Decisioning Python Code Node](#code)
* [Create a Dockerfile](#dockerfile)
* [Build and Start a SAS Container Runtime Container](#build)
* [Execute the Python Package Calling an Azure SQL Database](#exec)

---

## Prerequisites<a name="req"></a>

The following items are required before you begin this process:

* SAS Intelligent Decisioning with a Docker Repository configured as a publishing destination.
* An environment with Docker installed.
* Access to the Docker repository to pull and build the image.

## SAS Intelligent Decisioning Python Code Node <a name="code"></a>

The example data set `hmeq` can be found in [SAS Viya Datasets examples](https://support.sas.com/documentation/onlinedoc/viya/examples.htm). An additional column, `id`, was created as a Primary Key for this example.

The following Python code performs queries against an Azure SQL database. It must be inside a [Python Node](https://go.documentation.sas.com/doc/en/edmcdc/v_030/edmug/n04vfc1flrz8jsn1o5jblnbgx6i3.htm) in SAS Intelligent Decisioning.

```python
import pyodbc
import pandas as pd
import os 
import time
import logging

## Connection function, not directly called by SAS
def connect (retry_count = 0, n_retries = 20):
    server = 'py-scr.database.windows.net'
    database = 'scr-py'
    username = os.environ['db_username']
    password = os.environ['db_secret']
    driver= 'ODBC Driver 18 for SQL Server'
    retry = True

    while retry and retry_count <= n_retries:
        try:
            conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 
            retry = False
        except:
            retry_count = retry_count + 1
            logging.warning("WARNING: Initial connection failed, retry attempt " + str(retry_count))
            
            if retry_count == n_retries:
                raise Exception("Reconnection Failed " + retry_count + " times, aborting") 
                
            time.sleep(1)
    
    return conn

## Run once to setup the environment connection
conn = connect()

## Function that SAS calls
def execute (id):
    'Output:CLAGE,CLNO,DEBTINC,DELINQ,DEROG,JOB,LOAN,MORTDUE,NINQ,REASON,VALUE,YOJ'
    '''DependentPackages: pandas,pyodbc'''

    global conn

    retry = True

    query = "SELECT * FROM dbo.hmeq_id where id = " + str(id)
    
    while retry:
        try:
            user = pd.read_sql(query, conn)
            retry = False
        except:
            logging.warning("WARNING: Connection failed, retrying")
            conn = connect()

    LOAN = user["LOAN"].item()
    MORTDUE = user["MORTDUE"].item()
    VALUE = user["VALUE"].item()
    REASON = user["REASON"].values[0]
    JOB = user["JOB"].values[0]
    YOJ = user["YOJ"].item()
    DEROG = user["DEROG"].item()
    DELINQ = user["DELINQ"].item()
    CLAGE = user["CLAGE"].item()
    NINQ = user["NINQ"].item()
    CLNO = user["CLNO"].item()
    DEBTINC = user["DEBTINC"].item() 

    return CLAGE,CLNO,DEBTINC,DELINQ,DEROG,JOB,LOAN,MORTDUE,NINQ,REASON,VALUE,YOJ

```

### Notes:

1. The "DependentPackages" are installed with the container when published. Note that  `pyodbc` is required.

2. Since it is unlikely that the SAS Viya platform installation will include the Microsoft ODBC drivers along with the Python installation, the decision will not run in the context of the SAS Intelligent Decisioning user interface (CAS). It will run only through SAS Container Runtime.

## Create a Dockerfile<a name="dockerfile"></a>

After the previous node is added and published to a container destination, create a Dockerfile that will modify the container by installing the required ODBC drivers. Here is a sample script:

**Attention: Running this script automatically accepts two Microsoft End User License Agreements. If you are unfamiliar with these license agreements, you should reivew them.**

```sh
## If editing the Dockerfile created when published to Github remove the "FROM" row
FROM containerName:tag
USER root

RUN curl https://packages.microsoft.com/config/rhel/8/prod.repo > /etc/yum.repos.d/mssql-release.repo

## for microsoft odbc driver 17 use msodbcsql17 and mssql-tools
RUN ACCEPT_EULA=Y microdnf install -y msodbcsql18
RUN ACCEPT_EULA=Y microdnf install -y mssql-tools18

## for microsoft odbc driver 17 use $PATH:/opt/mssql-tools/bin
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
RUN source ~/.bashrc
RUN microdnf install -y unixODBC-devel
```

## Build and Start a SAS Container Runtime Container<a name="build"></a>

Navigate to the folder where the Dockerfile is located.

Use these commands to build the container:

```sh
docker build . -t scr-azure-name
```

Use these commands to start the container:

```sh
docker run --name scr_odbc \ 
           -e SAS_SCR_APP_PATH=/DecisionName \
           -e db_username=<dbUsername> \
           -e db_secret=<dbSecret> \  
           -p 8080:8080 decision_odbc
```

## Execute Python Package Calling Azure SQL Database<a name="exec"></a>

Submit the following JSON payload to SAS Container Runtime to execute the module. (Here is a sample endpoint: http://localhost:8080/DecisionName)

```json
{
  "data":
    {
    "id": 1337
    }
}
```

Here is a sample response:

```json
{
   "version" : 1,
   "metadata" : {
      "module_id" : "DecisionName",
      "step_id" : "execute",
      "timestamp" : "2023-01-16T15:11:42.549097Z",
      "elapsed_nanos" : 177900700
   },
   "data" : {
      "CLAGE": 149.195,
      "CLNO": 29,
      "DEBTINC": 37.8823,
      "DELINQ": 1,
      "DEROG": null,
      "JOB": "Other",
      "LOAN": 10600,
      "MORTDUE": 31216,
      "NINQ": 6,
      "REASON": "DebtCon", 
      "VALUE": 44716,
      "YOJ": 8
   }
}
```
