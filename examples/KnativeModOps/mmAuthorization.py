# Copyright (c) 2020, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import requests
import json
import os


os.environ['CAS_CLIENT_SSL_CA_LIST'] = '/sgrid/openssl_certs/cas_controller_certs/fsbudevviya4.fsbudev-openstack-k8s.unx.sas.com.pem'

os.environ['TKESSL_OPENSSL_LIB'] = '/usr/lib64/libssl.so.10'
os.environ['SSLREQCERT']='ALLOW'   

AUTHORIZATION_TOKEN = "Bearer "
AUTHORIZATION_HEADER = "Authorization"


class mmAuthorization(object):
    
    AUTHORIZATION_TOKEN = "Bearer "
    AUTHORIZATION_HEADER = "Authorization"
    
    uriAuth='/SASLogon/oauth/token'

    def __init__(self, params):
        """
        Constructor
        """

    def get_auth_token(self, url, user, password):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            }
        payload = 'grant_type=password&username=' + user + '&password=' + password
        auth_return = requests.post(url+self.uriAuth, data=payload, headers=headers,auth=('sas.ec', ''),verify=False)

        my_auth_json = json.loads(auth_return.content.decode('utf-8'))
        my_token = my_auth_json['access_token']
        return my_token

    
