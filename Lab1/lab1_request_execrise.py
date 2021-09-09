import requests

r = requests.get("https://raw.githubusercontent.com/nmrchvz/cmput404-labs/main/Lab1/lab1_request_execrise.py")
print(r.text)