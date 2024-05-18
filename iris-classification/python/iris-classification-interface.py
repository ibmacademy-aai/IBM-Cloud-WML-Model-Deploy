import gradio as gr
import requests

API_KEY = "API KEY KAMU"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


def predict_class(sepal_length, sepal_width, petal_length, petal_width):
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [
                                    "sepal_length",
                                    "sepal_width",
                                    "petal_length",
                                    "petal_width"
                            ], "values": [[sepal_length, sepal_width, petal_length, petal_width]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d42cd2d2-4dcc-44d3-8b28-9d09bb29a88c/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    response_values = response_scoring.json()['predictions'][0]['values']


    return response_values[0][0]

demo = gr.Interface(
    fn=predict_class,
    inputs=["number", "number", "number", "number"],
    outputs=[gr.Textbox(label="predicted as")],
)
if __name__ == "__main__":
    demo.launch()