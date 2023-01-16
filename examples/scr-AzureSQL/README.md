# Information about Accessing Azure SQL in SAS Container Runtime via Python

## Overview<a name="intro"></a>

This README contains information and instructions about how to access an Azure SQL database in SAS Container Runtime via a Python module. You can refer to [Azure's documentation](https://learn.microsoft.com/en-us/azure/azure-sql/database/connect-query-python?view=azuresql). Here are the tasks:

* [Requirements](#req)
* [SAS ID Python code node](#code)
* [Create a Dockerfile](#dockerfile)
* [Build SAS Container Runtime](#build)
* [Execute the SCR](#exec)

---

## Requirements<a name="req"></a>

- SAS Intelligent Decisioning with a Docker Repository as publishing destination configured
- An environment with docker installed and access to the Docker repository to pull and build the image

## Intelligent Decisioning Python code node <a name="code"></a>

The example dataset `hmeq` can be found in [SAS Viya Datasets examples](https://support.sas.com/documentation/onlinedoc/viya/examples.htm), an additional column was created as a Primary Key `id` for purpose of example.

Here is an example of Python code that performs queries against an Azure SQL database, and must be inside the [Python Node](https://go.documentation.sas.com/doc/en/edmcdc/v_030/edmug/n04vfc1flrz8jsn1o5jblnbgx6i3.htm) inside Intelligent Decisioning:


```python
import os
import pyodbc
import pandas

server = '<my.database.windows.net>'
database = '<database-name>'
username = os.environ['db_username'] ## Avoid hard coding
password = os.environ['db_secret'] ## Avoid hard coding
driver= '{ODBC Driver 18 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 

def execute (id):
    'Output:CLAGE,CLNO,DEBTINC,DELINQ,DEROG,JOB,LOAN,MORTDUE,NINQ,REASON,VALUE,YOJ'
    '''DependentPackages: pandas,pyodbc'''
	
    global conn
    
    query = "SELECT * FROM dbo.hmeq_id where id = " + str(id)
    user = pd.read_sql(query, conn)
    
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

1. This example does not cover retrying connection in case of failure/loss of connections. Alternatives are to move the connection string inside the `execution` function to be stablished every call (incurring performance issues) or having an error handler that recreates the connection if necessary.

2. The "DependentPackages" will be installed with the container when published, `pyodbc` is required.

3. Since it is unlikely that the Viya installation will include the Microsoft ODBC drivers along with the python installation, the decision will not run in the context o SAS Intelligent Decisioning UI (CAS), only through the SAS Container Runtime.

## Create a Dockerfile<a name="dockerfile"></a>

After the previous node has been added and published to a Container Destination, create a `Dockerfile` that will modify the container by installing the required ODBC drivers as follows:

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

Move to the folder where the `Dockerfile` is located.

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

## Execute Python Package Calling Azure SQL database<a name="exec"></a>

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
