import requests

url = 'http://127.0.0.1:5000/predict'
file_path = './tt csv artificial.CSV'

with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())