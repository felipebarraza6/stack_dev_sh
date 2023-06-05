from django.db.models import Count
from .models import (InteractionDetail, Client, ProfileClient)
from .serializers import InteractionDetailModelSerializer
import requests
from datetime import datetime
import pytz
from .send_data_dga import send
from django.core.serializers import json

def get_novus_and_send_api():
    clients = ProfileClient.objects.all()
    chile = pytz.timezone("America/Santiago")

    if(clients.count() > 0):

        for client in clients:

            if client.is_dga_medium:
                try:
                    get_data = InteractionDetail.objects.filter(profile_client=client.id).first()
                    response = {}
                    response["date_time_medition"] = datetime.now(chile).strftime("%Y-%m-%dT%H:00:00")
                    response["total"] = get_data.total
                    response["flow"] = get_data.flow
                    response["nivel"] = get_data.nivel
                    send(client, response)

                except Exception as e:
                    print(e)

    else:
        print('NO HAY CLIENTES CON SERVICIO DGA ESTANDAR MEDIO')


def main():
    get_novus_and_send_api()
