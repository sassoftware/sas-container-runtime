import csv
import json
import http.client
import re

def score_input_file(K8S_NAMESPACE, KNATIVE_SCORING_INGRESS_HOST,KNATIVE_SCORING_INGRESS_HOSTNAME, model_name, container_image_name, SCORE_INPUT_FILE, SCORE_OUT_FILE):

    int_pattern = re.compile("^[0-9]*$")
    float_pattern = re.compile("^[0-9]*.[0-9]*$")

    conn = http.client.HTTPConnection(KNATIVE_SCORING_INGRESS_HOST,80)

    # headers to make the http REST API call
    headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Host':model_name+"."+K8S_NAMESPACE+"."+KNATIVE_SCORING_INGRESS_HOSTNAME
            }

    one_time_headers=True
    with open(SCORE_INPUT_FILE,'r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        score_out_file = open(SCORE_OUT_FILE, 'w',  newline='')
        score_out_writer = csv.writer(score_out_file)

        # process each record in input file. Score and save o/p to output file.
        for record in reader:

            # the payload to REST API should follow format as in :
            # https://go.documentation.sas.com/doc/en/mascrtcdc/v_001/mascrtag/n12e5o7e0j8nipn1vtpjhuvcfdse.htm
            payload_list = []
            for key, value in record.items():

                # handle decimal values with thousand seperators and .'s
                int_pattern = re.compile("^[0-9]*$")
                float_pattern = re.compile("^[0-9]*.[0-9]*$")
                value_comma_removed_temp = value.replace(",","")

                if int_pattern.match(value_comma_removed_temp):
                    #print("value int match:", value, value_comma_removed_temp)
                    value = int(value_comma_removed_temp)

                if float_pattern.match(value_comma_removed_temp):
                    # ugly hack - remove later for not handling < and > in certain range fields.
                    if "<" in value_comma_removed_temp or ">" in value_comma_removed_temp:
                        pass
                    else:
                        #print("value float match:", value, value_comma_removed_temp)
                        value = float(value_comma_removed_temp)

                payload_list.append({"name": key, "value": value})

            #print("payload list: ", payload_list)
            payload = json.dumps({"inputs": payload_list})

            try:
                conn.request("POST","/"+container_image_name,payload,headers)
                resp_http = conn.getresponse()
                data = resp_http.read().decode("utf-8")
                #print("http response ", data)

                if "outputs" in json.loads(data).keys():
                    score_out = json.loads(data)["outputs"]
                else:
                    print("scoring request failed because input format not expected.")
                    print("data : ", data)
                    exit(1)

                col_names = []
                field_values = []
                for item in score_out:
                    col_names.append(item['name'])
                    field_values.append(item['value'])

                if one_time_headers:
                    score_out_writer.writerow(col_names)
                    one_time_headers = False

                score_out_writer.writerow(field_values)

            except Exception as e:
                print(str(e))
                raise e


