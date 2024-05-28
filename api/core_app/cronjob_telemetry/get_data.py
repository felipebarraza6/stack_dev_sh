
import datetime
import requests
import datetime
import requests
import smtplib
from .send_notify import send_mail_notified_not_conection


def thethings(token, variable, profile):
    try:
        url = f"https://api.thethings.io/v2/things/{
            token}/resources/{variable["str_variable"]}/?limit=1"
        response = requests.get(url, timeout=1000)
        response.raise_for_status()  # Check for any HTTP errors
        result = response.json()[0]['value']
        return result
    except requests.exceptions.RequestException as e:
        send_mail_notified_not_conection(profile, variable, e)
        return 0


def novuscloud(token, variable, profile):
    try:
        header = {"authorization": token}
        base_url_tago = f"https://api.tago.io/data/?variable={
            variable["str_variable"]}&query=last_item"
        response = requests.get(base_url_tago, headers=header, timeout=1000)
        response.raise_for_status()  # Check for any HTTP errors
        result = response.json()['result'][0]['value']
        return result
    except requests.exceptions.RequestException as e:
        send_mail_notified_not_conection(profile, variable, e)
        return 0
