from django.db.models import Count
from .models import (InteractionDetail, ProfileClient)
from .serializers import InteractionDetailModelSerializer, ProfileClientSerializer
import requests
from datetime import datetime
import pytz


def get_novus_and_save_in_api():
    clients = ProfileClient.objects.filter(is_monitoring=True)
    chile = pytz.timezone("America/Santiago")

    def parser_total(total, scale):
        """fx = (Delta Acumulado * P/LT) / 1000"""
        factor_total_scale = int(total) * int(scale)
        divide = int(factor_total_scale/1000)
        return divide


    for client in clients:
        response = {}
        client_serializer = ProfileClientSerializer(client).data
        response["date_time_medition"] = datetime.now(chile).strftime("%Y-%m-%dT%H:00:00")
        response["profile_client"] = client_serializer['id']

        for variable in client_serializer['variables']:
            token = client_serializer['token_service']

            if variable['is_other_token']:
                token = variable['token_service']

            parsed_url = ''

            if client_serializer['is_thethings']:
                parsed_url = (
                    f"https://api.thethings.io/v2/things/{token}/resources/{variable['str_variable']}/?limit=1"
                )
                request = requests.get(parsed_url)
            else:
                parsed_url = (
                    f"https://api.tago.io/data/?variable={variable['str_variable']}&query=last_item"
                )
                request = requests.get(parsed_url, headers={"authorization": token})


            data = request.json()

            if variable['type_variable'] == "ACUMULADO":
                if client_serializer['is_thethings']:
                    if data[0].get("value"):
                        response["total"] = parser_total(data[0].get("value"), client_serializer['scale'])
                    else:
                        response["total"] = "0"
                else:
                    if data.get("result"):
                        response["total"] = parser_total(data.get("result")[0].get("value"), client_serializer['scale'])
                    else:
                        response["total"] = "0"

            if variable['type_variable'] == "NIVEL":
                if client_serializer['is_thethings']:
                    if data[0].get("value"):
                        response["nivel"] = round(data[0].get("value"), 1)
                    else:
                        response["total"] = "0"
                else:
                    if data.get("result"):
                        response["nivel"] = data.get("result")[0].get("value")
                    else:
                        response["nivel"] = "0.0"
                
            if variable['type_variable'] == "CAUDAL":
                if client_serializer['is_thethings']:
                    if data[0].get("value"):
                        response["flow"] = round(data[0].get("value"), 1)
                    else:
                        response["flow"] = "0.0"
                else:
                    if data.get("result"):
                        response["flow"] = data.get("result")[0].get("value")
                    else:
                        response["flow"] = "0.0"

        if client_serializer['is_prom_flow']:
            get_last_data = InteractionDetail.objects.filter(profile_client=client_serializer['id']).first()

            last_total = 0
            if get_last_data is not None:
                last_total = get_last_data.total
                
            sustraction = int(response['total'])-int(last_total)
            prom_flow = float(sustraction / 3600)
            factor_to_mt = float(prom_flow*1000)
            response['flow'] = round(factor_to_mt, 1)

        serializer = InteractionDetailModelSerializer(data=response)
        serializer.is_valid(raise_exception=True)
        serializer.save()


def main():
    get_novus_and_save_in_api()
