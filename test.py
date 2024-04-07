import requests

# Assuming your Flask server is running locally on port 5000
url = "http://127.0.0.1:5000/chatbot"

# Example JSON data
data = {
    "symptoms": ['i am experiencing cough', 'fever', 'i am experiencing headache']
}

# Sending POST request to the Flask API
response = requests.post(url, json=data)

print(response.json())