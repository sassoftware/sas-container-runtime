# Author Sudhir Reddy @ SAS
# 
###------------------------------------------
# 
# This script launch two daemons both webservers.
#
# 1. SCR REST API server. This should correcpond to ENTRYPOINT set in original SCR container image
# we need to set java.io.tmpdir as sagemaker invoked docker containers (secured ones) do not let you write to /tmp.
# Also override the port to 9090 as original 8080 is called by sagemaker. 

export _JAVA_OPTIONS=-Djava.io.tmpdir=/opt/tmp
#export CATALINA_BASE=/opt
#export CATALINA_TMPDIR=/opt/tmp
/usr/lib/jvm/jre/bin/java -Xrs -cp /opt/scr/viya/home/solo:/opt/scr/viya/home/solo/lib/* com.sas.mas.solo.Application -Djava.library.path=/opt/scr/viya/home/SASFoundation/sasexe --server.port=9090 &
#------
# 2.Launches python server which basically does redirects to SCR server. Sagemaker inference mandates /invocations and /ping URI which is not supported by SCR REST API server.
# that is the background of this second daemon
gunicorn --bind 0.0.0.0:8080 sagemaker_server:app &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?

