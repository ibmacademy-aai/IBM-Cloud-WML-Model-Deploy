import requests
import cv2
import numpy as np

def preprocess_image(image_path):
  # Membaca gambar
  image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

  # Mengubah ukuran gambar menjadi 28x28 piksel
  image = cv2.resize(image, (28, 28))

  # Mengubah gambar menjadi array NumPy
  image = np.array(image)
  
  # melakukan inversi warna
  image = cv2.bitwise_not(image)
  return image

# Contoh penggunaan
image_path = "./test_image/Screenshot 2024-05-18 174736.png"
preprocessed_data = preprocess_image(image_path)
test_data = preprocessed_data.flatten().tolist()

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account (https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-authentication.html)
API_KEY = "API KEY KAMU"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [], "values": [test_data]}]} # mengirimkan data gambar yang sudah di flatten dari 28x28 pixel jadi array dengan panjang 784  

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/bf506f75-1262-4cc9-ad9c-fb2d2cda377f/predictions?version=2021-05-01', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")

# menamppilkan hasil klasifikasi
response_values = response_scoring.json()['predictions'][0]['values'][0][1]

print(response_values)