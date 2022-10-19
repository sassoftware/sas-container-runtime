# Information about Accessing DB2 in SAS Container Runtime via Python

## Overview<a name="intro"></a>

This README contains information and instructions about how to access a DB2 database in SAS Container Runtime via a Python module. Here are the tasks:

* [Obtain the Required Libraries](#libreq)
* [Obtain and Configure the Required Python Package](#pythonpkgreq)
* [Add the Required Items to the Dockerfile](#addreq)
* [Review Sample Python Package Code](#code)
* [Build SAS Container Runtime](#build)
* [Execute Python Package Code](#exec)

This README also includes information about how to [Access DB2 via Python without SAS Container Runtime](#other).

---

## Obtain the Required Libraries<a name="libreq"></a>

* gcc: GCC (GNU Compiler Collection) is an integrated distribution of compilers for several major programming languages. These languages currently include C, C++, Objective-C, Objective-C++, Java, Fortran, and Ada.

* python3-devel: This package contains the header files and configuration that you need to compile Python extension modules (typically written in C or C++), to embed Python into other programs, and to make binary distributions for Python libraries.

* libpam.so.0: A pluggable authentication module (PAM) library.

## Obtain and Configure the Required Python Package<a name="pythonpkgreq"></a>

You must add the ibm-db Python package to the requirements.txt file in order to pick up the IBM DB2 library. 

Here is an example: "ibm-db==3.0.1"

## Add the Required Items to the Dockerfile<a name="addreq"></a>

Here is a Dockerfile sample that shows the Python configuration and installation of the required libraries:

```sh
COPY mas2py.py /mas2py/mas2py.py
USER root
RUN microdnf -y install gcc
RUN microdnf -y install python3-devel
RUN microdnf -y install libpam.so.0
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt 
ENV MAS_PYPATH=/usr/bin/python3
ENV MAS_M2PATH=/mas2py/mas2py.py
```

## Review Sample Python Package Code<a name="code"></a>

Here is an example of Python package code that performs queries against a DB2 database:

```sh
import ibm_db\n
def execute():\n
    'Output: outString'\n
    conn = ibm_db.connect(\"DATABASE=rtdm HOSTNAME=db2dmops2.unx.sas.com PORT=50001 PROTOCOL=TCPIP UID=***** PWD = *****\", \"\", \"\")\n
    ibm_db.exec_immediate(conn, \"DROP Table Users\")\n
    ibm_db.exec_immediate(conn, \"CREATE TABLE Users (uid int, lname varchar(255), fname varchar(255))\")\n
    ibm_db.exec_immediate(conn, \"INSERT INTO Users values(404, 'Simpson', 'Homer')\")\n
    ibm_db.exec_immediate(conn, \"INSERT INTO Users values(555, 'Burns', 'Montgomery')\")\n
    ibm_db.exec_immediate(conn, \"INSERT INTO Users values(99, 'Simpson', 'Maggie')\")\n
    stmt = ibm_db.exec_immediate(conn, \"SELECT * FROM Users WHERE uid = 404\")\n
    while ibm_db.fetch_row(stmt) is True:\n
        outString = ibm_db.result(stmt, 1)\n
    return outString\n
```

## Build and Start a SAS Container Runtime Container<a name="build"></a>

Use these commands to build and start the container:

```sh
docker compose build
docker compose up
```

## Execute Python Package Calling DB2<a name="exec"></a>


Submit the following JSON payload to SAS Container Runtime to execute the module. (Here is a sample endpoint: http://localhost:8080/execute/execute)

```sh
{
  "data":
    {
    }
}
```

Here is a sample response:

```sh
{
   "version" : 1,
   "metadata" : {
      "module_id" : "execute",
      "step_id" : "execute",
      "timestamp" : "2022-06-17T12:48:22.773Z",
      "elapsed_nanos" : 66075600
   },
   "data" : {
      "outString" : "Simpson"
   }
}
```

### Access DB2 via Python without SAS Container Runtime<a name="other"></a>

Here is an example of stand-alone Python code that accesses DB2 without SAS Container Runtime:

```sh
import ibm_db


class TestDB2:
    def test_select(self):
        conn = ibm_db.connect("DATABASE=rtdm;HOSTNAME=db2dmops2.unx.sas.com;PORT=50001;PROTOCOL=TCPIP;UID=*****;PWD = *****;", "", "")
        ibm_db.exec_immediate(conn, "DROP Table Users")
        ibm_db.exec_immediate(conn, "CREATE TABLE Users (uid int, lname varchar(255), fname varchar(255))")
        ibm_db.exec_immediate(conn, \"INSERT INTO Users values(404, 'Simpson', 'Homer')\")\n
        ibm_db.exec_immediate(conn, \"INSERT INTO Users values(555, 'Burns', 'Montgomery')\")\n
        ibm_db.exec_immediate(conn, \"INSERT INTO Users values(99, 'Simpson', 'Maggie')\")\n
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM Users WHERE lname = 'Simpson'")
        while ibm_db.fetch_row(stmt) is True:
            uid = ibm_db.result(stmt, 0)
            lname = ibm_db.result(stmt, 1)
            fname = ibm_db.result(stmt, 2)
            print("--------------------")
            print("uid: ", uid)
            print("lname: ", lname)
            print("fname: ", fname)
```