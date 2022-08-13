import requests
import zeep
import pytz
from datetime import datetime
from .crm.models import ProfileClient 
from .crm.serializers import InteractionDetailSerializer


list_variables = {
    "nivel": "3grecuc2v",
    "acumulado": "3grecdi1va",
    "caudal": "3grecuc1v",
}

list_productos = ProfileClient.objects.all().values()

def get_values(token):
    response = {}
    for item in list_variables.keys():
        parsed_url = (
            f"https://api.tago.io/data/?variable={list_variables[item]}&query=last_item"
        )
        request = requests.get(parsed_url, headers={"authorization": token})
        data = request.json()
        chilean_timezone = pytz.timezone("America/Santiago")
        date_now = datetime.now(chilean_timezone)
        response["date_time_medition"] = date_now 
        if item == "nivel":
            print(data.get("result")>0)
            response["nivel"] = data.get("result")[0].get("value")
        elif item == "caudal":
            response["flow"] = data.get("result")[0].get("value")
        else:
            response["total"] = data.get("result")[0].get("value")

    return response


def run_interactions():
    #  obtiene listado de predios
    wsdl = 'https://snia.mop.gob.cl/controlextraccion/wsdl/datosExtraccion/SendDataExtraccionService?wsdl'
    client = zeep.Client(wsdl=wsdl)
    print(dir(client.service.authSendDataExtraccionOp.authDataUsuario()))

    response = []
    for item in list_productos:
        data = get_values(item['token_service'])
        retrieve = ProfileClient.objects.filter(id=item['id']).first()
        data["profile_client"] = retrieve.id
        response.append(data)

    for item in response:
        serializer = InteractionDetailSerializer(data=item)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("guardado")
    return {"data":response}


def main():
    interaction=run_interactions()
