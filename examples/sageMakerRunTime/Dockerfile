# Author : Sudhir Reddy @ SAS
#########
# Using SCR image as the base image 
#
# Following variable to be replaced
# REPLACE_KEY_1
FROM 617292774228.dkr.ecr.us-east-1.amazonaws.com/sunallscrtree1
 
#Installing python packages 
USER root
#------------------------- Temp for debugging. Comment after usage as they make image bigger
#RUN microdnf install yum 
#RUN yum install -y procps
#-----------------
# sagemaker containers could not write  to /tmp. So used /opt/tmp in its place.
RUN /bin/bash -c 'mkdir sagemaker ; mkdir /opt/tmp; chmod -R 777 /opt/tmp'
WORKDIR /sagemaker
RUN /bin/bash -c 'python -m ensurepip --upgrade; pip3 install flask gunicorn urllib3'
 
# Copy the models directory and server.py files
ADD sagemaker_server.py sagemaker_server.py
ADD launch_two_servers.sh launch_two_servers.sh
RUN chmod a+x launch_two_servers.sh

# Switch back to "sas user" which is set in base image
USER 1001:0

#Exposing the port from the container. Two ports. 
# 8080 used by gunicorn which is called by sagemaker runtime
# 9090 used by scr rest api tomcat server
EXPOSE 8080
EXPOSE 9090

#----
# Following set let us test this feature from standalone docker testing in non-sagemaker setting testing 
#ENTRYPOINT ["/usr/bin/env"]
#CMD ["/sagemaker/launch_two_servers.sh"] 
# 
# following is required for sagemaker inference. 
# Sagemaker calls container entrypoint with "docker run image serve" where serve overrides  CMD arguments
# So came with following . In this case "serve" command argument does not serve any purpose
# ENTRYPOINT receives serve argument but ignores it 
ENTRYPOINT ["/usr/bin/env","/sagemaker/launch_two_servers.sh"]

