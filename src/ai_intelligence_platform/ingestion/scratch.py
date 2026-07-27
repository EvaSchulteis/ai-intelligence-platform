import requests

def inspect_response():
    response = requests.get("https://api.github.com")

    print(type(response))
    print(type(response.json()))
    print(response.status_code)

    print(type(response.status_code))
    print(type(response.text))
    print(type(response.headers))