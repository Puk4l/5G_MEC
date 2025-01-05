import requests

# Example input data (from your dataset)
input_data = {
    'Application_Type': 1,  # Replace with actual data from your dataset
    'Signal_Strength': -50,
    'Latency': 30,
    'Required_Bandwidth': 10,
    'Allocated_Bandwidth': 8
}

# Send a POST request to the container's /predict endpoint
url = 'http://localhost:5000/predict'
response = requests.post(url, json=input_data)

# Check if the response was successful
if response.status_code == 200:
    output = response.json()
    print(f"Input Data: {input_data}")
    print(f"Prediction: {output['prediction']}")
else:
    print(f"Error: {response.status_code}, {response.text}")
