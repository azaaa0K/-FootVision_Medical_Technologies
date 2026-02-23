import requests

url = "https://percolative-glennis-gainfully.ngrok-free.dev/api/dfu"

# Make sure 'foot.jpg' exists in the same folder as testy.py
files = {'image': ('foot.jpg', open('foot.jpg', 'rb'), 'image/jpeg')}
data = {'name': 'Ahmed Khan', 'symptoms': 'pain'}

response = requests.post(url, files=files, data=data)
print(response.json())