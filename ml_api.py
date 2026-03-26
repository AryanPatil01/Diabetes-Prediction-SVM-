from fastapi import FastAPI
from pydantic import BaseModel    
import pickle
import json
app = FastAPI()
class InputData(BaseModel):
    pregnancies	: int
    Glucose	: int
    BloodPressure	: int
    SkinThickness	: int
    Insulin	: int
    BMI	: float
    DiabetesPedigreeFunction	: float
    Age	: int

# Load the trained model
trained_diabetes_model = pickle.load(open('trained_diabet_model.sav', 'rb'))
trained_standard_scaler = pickle.load(open('trained_diabet_scalar.sav', 'rb'))

@app.post("/diabetes_predict")
async def diabeted_pred(data: InputData):
    # Convert input data to a list for prediction
    input_data = data.model_dump_json()
    input_data_dict = json.loads(input_data)
    input_data_list = [input_data_dict['pregnancies'], input_data_dict['Glucose'], input_data_dict['BloodPressure'], input_data_dict['SkinThickness'], input_data_dict['Insulin'], input_data_dict['BMI'], input_data_dict['DiabetesPedigreeFunction'], input_data_dict['Age']]
    # Scale the input data using the trained standard scaler     
    scaled_input_data = trained_standard_scaler.transform([input_data_list])
    # Make a prediction using the trained model
    prediction = trained_diabetes_model.predict(scaled_input_data)
    # Return the prediction result
    if prediction[0] == 1:
        return {"prediction": "The person is likely to have diabetes."}
    else:
        return {"prediction": "The person is unlikely to have diabetes."}
 