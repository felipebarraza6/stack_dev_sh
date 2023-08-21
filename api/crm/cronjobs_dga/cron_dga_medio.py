from django.db.models import Count
from ..models import (InteractionDetail, ProfileClient)
from datetime import datetime
import pytz
from .send_data_dga import send
from django.utils import timezone
hora_actual = timezone.now()


def get_novus_and_send_api():
    print(hora_actual)
    clients = ProfileClient.objects.filter(standard='MEDIO', is_send_dga=True)
    chile = pytz.timezone("America/Santiago")
    print(clients)
    if(clients.count() > 0):
        for client in clients:
            try:
                get_data = InteractionDetail.objects.filter(profile_client=client.id).first()
                response = {}
                response["date_time_medition"] = datetime.now(chile).strftime("%Y-%m-%dT%H:00:00")
                response["total"] = get_data.total
                response["flow"] = get_data.flow
                response["nivel"] = get_data.nivel
                response['id_data'] = get_data.id
                send(client, response)
            except Exception as e:
                print(e)
    else:
        print('NO HAY CLIENTES CON SERVICIO DGA ESTANDAR MEDIO')


def main():
    get_novus_and_send_api()
