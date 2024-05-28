from ..models import InteractionDetail
from .send_notify import send_mail_notify
import json
from ..serializers import (
    InteractionDetailModelSerializer)


def data_processing(response, client_serializer):
    scale = client_serializer['scale']
    counter_acum = client_serializer['counter_acum']
    is_prom_flow = client_serializer['is_prom_flow']

    response['total'] = parser_total(
        response['ACUMULADO'], scale, counter_acum)
    response['nivel'] = round(float(response['NIVEL']), 1)

    if is_prom_flow is False:
        response['flow'] = round(float(response['CAUDAL']), 1)
        response = {key: value for key,
                    value in response.items() if key != 'CAUDAL'}
    else:
        count_data = InteractionDetail.objects.filter(
            profile_client=client_serializer['id']).count()
        if count_data <= 0:
            response['flow'] = 0.0
        else:
            get_last_data = InteractionDetail.objects.filter(
                profile_client=client_serializer['id']).first()
            last_total = get_last_data.total
            sustraction = int(response['total']) - int(last_total)
            if sustraction < 0:
                response['flow'] = 0.0
            else:
                prom_flow = float(sustraction / 3600)
                factor_to_mt = float(prom_flow * 1000)
                response['flow'] = round(factor_to_mt, 1)

    response = {key: value for key,
                value in response.items() if key != 'CAUDAL'}
    response = {key: value for key, value in response.items() if key !=
                'ACUMULADO'}
    response = {key: value for key,
                value in response.items() if key != 'NIVEL'}

    validator(response, client_serializer)

    serializer = InteractionDetailModelSerializer(data=response)
    serializer.is_valid(raise_exception=True)
    serializer.save()


def parser_total(total, scale, counter):
    """Local Constant."""
    factor_total_scale = int(total * scale)
    divide = int(factor_total_scale / 1000)
    add_counter = int(divide) + int(counter)
    return add_counter


def validator(response, client_serializer):
    txt_error = ""
    nivel = response['nivel']
    caudal = response['flow']
    total = response['total']

    last_data = InteractionDetail.objects.filter(
        profile_client=client_serializer['id']).first().total
    if nivel < 0:
        txt_error += "nivel menor a 0.0\n"
    if caudal < -2.0:
        txt_error += "flujo menor a -2.0\n"
    if total < 0:
        txt_error += "total menor a 0\n"
    if total < int(last_data):
        txt_error += "total menor a su última captación\n"

    if txt_error:
        send_mail_notify(client_serializer, response, txt_error)
