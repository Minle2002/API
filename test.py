import requests

url = "https://api-nts4.onrender.com/chatbot"

# Example JSON data
data = {
    "symptoms": ['i am experiencing cough', 'fever', 'i am experiencing headache']
}

response = requests.post(url, json=data)

print(response.json())