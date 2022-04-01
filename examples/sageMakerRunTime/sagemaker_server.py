## Author: Sudhir Reddy @ SAS
## Serves as additional  webserver to reduirect requests to original java SCR server
## Redirects required by sagemaker requirements to serve custom model containers
##------
from flask import Flask, Response, request, redirect, render_template
from urllib.parse import urlparse
import http.client
import json

# SCR model name
#SCR_MODEL_NAME = "sunallscrtree1"
# REPLACE_KEY_2
SCR_MODEL_NAME = 'sunallscrtree1'

app = Flask(__name__)
app.config['DEBUG'] = True

headers = {
           'Accept': 'application/json',
           'Content-Type': 'application/json',
          }


@app.route('/invocations',methods=['POST'])
def redirect_to_scr():
    # First way - Just do a redirect to original SCR tomcat server.
    # This failed because sagemaker runtime client cannot handle redirects unlike say "curl --location"
    #curr_base_url = urlparse(request.base_url)
    #host_url = (curr_base_url.netloc).split(':')[0]
    #new_base_url = "http://" + host_url + ":9090" + "/" + SCR_MODEL_NAME
    #return f'Hello SCR! , {new_base_url}'
    #return redirect("http://localhost:9090/sunallscrtree1", code=307)
    #return redirect(new_base_url, code=308)

    # Second way. This server acts as both a http client and http server. This one becomes a http client
    # to make calls to original SCR REST API server on 9090.
    payload = request.get_json()
    conn = http.client.HTTPConnection("localhost",9090)
    payload_to_scr  = json.dumps(payload)

    try:
       conn.request("POST","/"+SCR_MODEL_NAME,payload_to_scr,headers)
       resp_http = conn.getresponse()
       #return payload
       data = resp_http.read().decode("utf-8")
       return data

    except Exception as e:
       return "Exception raised in try block. Investigate.."
       #return str(e).encode("ascii")


@app.route('/ping',methods=['GET'])
def ping_scr():
    #return 'Hello SCR!'
    # This should really test SCR server availability before setting this but I woould leave to customer on how to implement this.
    # Do they want to put more load with all pings issued by sagemaker for each second? I leave it for now.
    return Response(status = 200)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
