from django.db.models import Count
from .models import InteractionDetail, ProfileClient
from .serializers import InteractionDetailModelSerializer, CronProfileClientSerializer
import requests
from datetime import datetime
import pytz


def get_novus_and_save_in_api():
    clients = ProfileClient.objects.filter(is_monitoring=True).order_by('created')
    chile = pytz.timezone("America/Santiago")

    def parser_total(total, scale, profile, variable):
        """fx = (Delta Acumulado * P/LT) / 1000"""
        old_data = InteractionDetail.objects.filter(profile_client=profile["id"]).first()
        factor_total_scale = int(total) * int(scale)
        divide = int(factor_total_scale/1000)
        return int(divide + variable['counter'])

    for client in clients:
        response = {}
        client_serializer = CronProfileClientSerializer(client).data
        response["date_time_medition"] = datetime.now(
            chile).strftime("%Y-%m-%dT%H:00:00")
        response["profile_client"] = client_serializer['id']

        original_thethings = client_serializer["is_thethings"]

        for variable in client_serializer['variables']:
            token = client_serializer['token_service']

            if variable['is_other_token']:
                token = variable['token_service']

            if variable["is_other_url"]:
                client_serializer["is_thethings"] = not client_serializer["is_thethings"]
            else:
                client_serializer["is_thethings"] = original_thethings
                    
            if client_serializer['is_thethings']:
                parsed_url = (
                    f"https://api.thethings.io/v2/things/{token}/resources/{variable['str_variable']}/?limit=1"
                )
                request = requests.get(parsed_url)
                if variable['type_variable'] == "ACUMULADO":
                    data = request.json()
                    if data and data[0].get("datetime"):
                        response["date_time_last_logger"] = data[0].get("datetime")
            else:
                parsed_url = (
                    f"https://api.tago.io/data/?variable={variable['str_variable']}&query=last_item"
                )
                request = requests.get(parsed_url, headers={
                                       "authorization": token})

                if variable['type_variable'] == "ACUMULADO":
                    data = request.json()
                    if "result" in data and len(data["result"]) > 0:
                    # Accede al primer elemento en 'result'
                        primer_elemento = data["result"][0]
                        if "time" in primer_elemento:
                            valor_time = primer_elemento["time"]
                            response["date_time_last_logger"] = valor_time



            data = request.json()

            if variable['type_variable'] == "ACUMULADO":
                if client_serializer['is_thethings']:
                    if data and data[0].get("value"):
                        response["total"] = parser_total(
                            data[0].get("value"), client_serializer['scale'], client_serializer, variable)
                    else:
                        response["total"] = "0"
                else:
                    if data and data.get("result"):
                        response["total"] = parser_total(
                            data.get("result")[0].get("value"), client_serializer['scale'], client_serializer, variable)
                    else:
                        response["total"] = "0"

            if variable['type_variable'] == "NIVEL":
                if client_serializer['is_thethings']:
                    if data and data[0].get("value"):
                        response["nivel"] = round(data[0].get("value"), 1)
                    else:
                        response["nivel"] = "0"
                else:
                    if data and data.get("result"):
                        response["nivel"] = data.get("result")[0].get("value")
                    else:
                        response["nivel"] = "0.0"

            if variable['type_variable'] == "CAUDAL":
                if client_serializer['is_thethings']:
                    if data and data[0].get("value"):
                        response["flow"] = round(data[0].get("value"), 1)
                        if variable['convert_to_lt']:
                            response["flow"] = round(data[0].get("value") / 3.6, 1) 

                    else:
                        response["flow"] = "0.0"
                else:
                    if data and data.get("result"):
                        response["flow"] = data.get("result")[0].get("value")
                        if variable['convert_to_lt']:
                            response["flow"] = round(data.get("result")[0].get("value") / 3.6, 1) 
                    else:
                        response["flow"] = "0.0"

        if client_serializer['is_prom_flow']:
            get_last_data = InteractionDetail.objects.filter(
                profile_client=client_serializer['id']).last()

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

