from django.db.models import Count
from ..models import (InteractionDetail, ProfileClient)
from ..serializers import InteractionDetailModelSerializer
from datetime import datetime
import pytz
from .send_data_dga import send

def get_novus_and_send_api():
    clients = ProfileClient.objects.filter(standard='CAUDALES_MUY_PEQUENOS', is_send_dga=True)
    chile = pytz.timezone("America/Santiago")
    day = datetime.now(chile).strftime("%d")
    month = datetime.now(chile).strftime("%m")
    year = datetime.now(chile).strftime("%Y")
    hour = datetime.now(chile).strftime("%H")

    if(clients.count() > 0):
        for client in clients:
            try:
                get_data = InteractionDetail.objects.filter(profile_client=client.id).first()
                response = {}
                if client.is_prom_flow:
                    get_data_old = InteractionDetail.objects.filter(
                        profile_client=client.id,
                        date_time_medition__year=int(year)-1,
                        date_time_medition__month=month,
                        date_time_medition__day=day,
                        date_time_medition__hour=hour
                    ).first()
                    last_total = 0
                    if get_data_old is not None:
                        last_total = int(InteractionDetailModelSerializer(get_data_old).data['total'])

                    total_old = last_total
                    sustraction = int(get_data.total) - total_old
                    prom_flow = float(sustraction / 31536000)
                    factor_to_mt = float(prom_flow*1000)
                    response["flow"] = round(factor_to_mt, 1)
                else:
                    response["flow"] = get_data.flow
                response["date_time_medition"] = datetime.now(chile).strftime("%Y-%m-%dT%H:00:00")
                response["total"] = get_data.total
                response["nivel"] = get_data.nivel
                response['id_data'] = get_data.id
                send(client, response)
            except Exception as e:
                print(e)
    else:
        print('NO HAY CLIENTES CON SERVICIO DGA ESTANDAR CAUDALES MUY PEQUENOS')


def main():
    get_novus_and_send_api()