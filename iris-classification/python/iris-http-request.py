import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account (https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-authentication.html)
API_KEY = "API KEY KAMU"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
#             SL    SW    PL    PW
test_data1 = [5.1,  3.5,  1.4,  0.2]
test_data2 = [6.5,  3,    5.8,  2.2]
test_data3 = [6.6,  2.9,  4.6,  1.3]

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [
                                "sepal_length",
                                "sepal_width",
                                "petal_length",
                                "petal_width"
                        ], "values": [[5.1,3.5,1.4,0.2], [6.5,3,5.8,2.2], [6.6,2.9,4.6,1.3]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d42cd2d2-4dcc-44d3-8b28-9d09bb29a88c/predictions?version=2021-05-01', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
response_values = response_scoring.json()['predictions'][0]['values']

print("data 1 species : ", response_values[0])
print("data 2 species : ", response_values[1])
print("data 3 species : ", response_values[2])