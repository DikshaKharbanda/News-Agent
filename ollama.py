import requests

# Define the API key and endpoint
api_key = "AIzaSyCw2B5ou8onk1BabogyppBYX_Ff2oalQ00"  # Replace with your actual API key
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

# Set the headers
headers = {
    "Content-Type": "application/json",
}

# Define the payload
payload = {
    "contents": [
        {
            "parts": [
                {"text": "Explain how AI works"}
            ]
        }
    ]
}

# Make the POST request
response = requests.post(url, headers=headers, json=payload)

# Handle the response
if response.status_code == 200:
    print("Response:", response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
