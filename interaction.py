import requests


def main():
    print("aaaa")
    response= requests.get("0.0.0.0:8000/api/client_profile/create_interaction/")
    print(response.json())