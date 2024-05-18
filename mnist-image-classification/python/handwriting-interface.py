import gradio as gr
import cv2
import numpy as np
import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account (https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-authentication.html)
API_KEY = "API KEY KAMU"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



def preprocess_image(image):
  image = np.array(image)
  # mengubah gambar input jadi grayscale
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # mengubah size jadi 28x28 piksel
  image = cv2.resize(image, (28, 28))
  image = np.array(image)
  # melakukan inversi warna
  image = cv2.bitwise_not(image)

  return image


def image_classifier(image):
    preprocessed_data = preprocess_image(image)
    test_data = preprocessed_data.flatten().tolist()
    payload_scoring = {"input_data": [{"fields": [], "values": [test_data]}]} # mengirimkan data gambar yang sudah di flatten dari 28x28 pixel jadi array dengan panjang 784 

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/bf506f75-1262-4cc9-ad9c-fb2d2cda377f/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")

    predicted_class = response_scoring.json()['predictions'][0]['values'][0][1]
    return predicted_class

demo = gr.Interface(fn=image_classifier, inputs="image", outputs=[gr.Textbox(label="predicted class")])
demo.launch()