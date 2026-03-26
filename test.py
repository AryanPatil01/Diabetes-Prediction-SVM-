import json 
import requests
url = "http://127.0.0.1:8000/diabetes_predict"
data = {
    "pregnancies": 2,
    "Glucose": 120,
    "BloodPressure": 70,
    "SkinThickness": 20,
    "Insulin": 85,
    "BMI": 30.5,
    "DiabetesPedigreeFunction": 0.5,
    "Age": 45
}
input_data_json = json.dumps(data)

response = requests.post(url, data=input_data_json, headers={'Content-Type': 'application/json'})    
print(response.text)
