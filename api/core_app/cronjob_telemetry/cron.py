"""Servicio principal de telemetría"""
from datetime import datetime
import pytz
from ..models import ProfileClient
from ..serializers import CronProfileClientSerializer
# Procesadores de datos
from .validators import data_processing
# Servicios externos de consulta de información de loggers
from .get_data import thethings, novuscloud


def main():
    clients = ProfileClient.objects.filter(is_monitoring=True, frecuency=60)
    chile = pytz.timezone("America/Santiago")
    response = {}

    for client in clients:
        client_serializer = CronProfileClientSerializer(client).data
        response["date_time_medition"] = datetime.now(
            chile).strftime("%Y-%m-%dT%H:00:00")
        response["profile_client"] = client_serializer['id']
        for variable in client_serializer['variables']:
            if variable['is_other_token'] is False:
                variable['token_service'] = client_serializer['token_service']
                variable['service'] = "thethings" if client_serializer['is_thethings'] else "novus"
            else:
                if variable['is_other_url']:
                    variable['service'] = "novus" if client_serializer['is_thethings'] else "thethings"

            if variable['type_variable'] == "ACUMULADO":
                client_serializer['counter_acum'] = variable['counter']

            if variable['service'] == "thethings":
                response[variable['type_variable']] = thethings(
                    variable['token_service'], variable, client_serializer)
            else:
                response[variable['type_variable']] = novuscloud(
                    variable['token_service'], variable, client_serializer)

        data_processing(response, client_serializer)


if __name__ == "__main__":
    main()
