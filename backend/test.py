import requests as re
import json

req=re.post('http://localhost:8000/api/register/', data={'email': 'ankamsaiteja27+1@gmail.com','otp':'289658','password':'your_password','full_name':'Your Name','phone_number':'1234567890'})
print(req.json())