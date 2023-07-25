FROM repulpmaster.unx.sas.com/viya-4-x64_oci_linux_2-docker-testready/sas-mas-solo-base-builder:1.64.34-20230718.1689698013581 as base
FROM repulpmaster.unx.sas.com/viya-4-x64_oci_linux_2-docker-testready/sas-decisions-runtime-base:1.56.31-20230718.1689700911455

EXPOSE 8080

WORKDIR /modules
COPY ./modules .
VOLUME /modules
RUN ls -al

USER root
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt 
