from django.db.models import Count
from .models import (InteractionDetail, User, Client, ProfileClient)
from .serializers import InteractionDetailModelSerializer
import requests
from datetime import datetime
from zeep import Client
import pytz
from .send_data_dga import send

def get_novus_and_save_in_api():
    clients = ProfileClient.objects.all()
    chile = pytz.timezone("America/Santiago")

    for client in clients:
        list_variables = {
            "nivel": "3grecuc2v",
            "acumulado": "3grecdi1va",
            "caudal": "3grecuc1v",
        }

        response = {}
        for variable in list_variables.keys():
            parsed_url = (
                f"https://api.tago.io/data/?variable={list_variables[variable]}&query=last_item"
            )

            request = requests.get(parsed_url, headers={"authorization": client.token_service})

            data = request.json()

            response["date_time_medition"] = datetime.now(chile).strftime("%Y-%m-%dT%H:00:00")
            response["profile_client"] = client.id

            if variable == "nivel":
                if data.get("result"):
                    response["nivel"] = data.get("result")[0].get("value")
                else:
                    response["nivel"] = "0.0"
            if variable == "caudal":
                if data.get("result"):
                    response["flow"] = data.get("result")[0].get("value")
                else:
                    response["flow"] = "0.0"
            if variable == "acumulado":
                if data.get("result"):
                    response["total"] = data.get("result")[0].get("value")
                else:
                    response["total"] = "0"

        serializer = InteractionDetailModelSerializer(data=response)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Eliminar los registros duplicados basados en el campo 'total'
        # Obtener una consulta con los registros duplicados
        duplicates = InteractionDetail.objects.values('date_time_medition').annotate(count=Count('date_time_medition')).filter(count__gt=1)

        # Eliminar los registros duplicados excepto uno
        for duplicate in duplicates:
            InteractionDetail.objects.filter(total=duplicate['date_time_medition']).exclude(
                id=InteractionDetail.objects.filter(total=duplicate['date_time_medition']).earliest('date_time_medition').id).delete()




def main():
    get_novus_and_save_in_api()
