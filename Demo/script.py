import requests
import time


url_POST = 'http://127.0.0.1:5000/register_user'
url_GET = 'http://127.0.0.1:5000/get_user_attributes'

name = "Hamdiata Diakite"
username = 'hamdiatadiakite'
user_email = 'hamdiatadiakite@cmail.carleton.ca'
phone_number = '819-213-6364'
password = 'SYSC3010'

# Data to be sent
data = {
    'name': name,
    'username': username,
    'email': user_email,
    'phone_number': phone_number,
    'password': password
   
}

print("Making POST request")
time.sleep(1)
response = requests.post(url_POST, json=data)
if response.status_code == 200:
       print("POST request sucessful, user added to database")
    
else:
    print(response.status_code)
    
    time.sleep(1)
    


    
# Test that we are able get email we just added    
params = {
    'username': username,
    'attribute': 'email'
}

# Send GET request to the server
print("Making GET request")
time.sleep(1)
response = requests.get(url_GET, params=params)
user_attribute = response.json()

retreived_email_adress = user_attribute.get('email')

# Check if request was successful 
if response.status_code == 200:
    print("GET request sucessful")
   
else:
    print(response.status_code)

if user_email == retreived_email_adress:
    print(f"User email is: {user_email}")
    time.sleep(1)
    print(f"Email retrieved from database is: {retreived_email_adress}")
    time.sleep(1)
    print("Test sucesfull")
else:
    print("Test failed")






