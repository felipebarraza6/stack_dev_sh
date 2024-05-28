from zeep import Client
import requests
import xml.etree.ElementTree as ET
from ..models import InteractionDetail


def send(profile_data, response):

    def convertir_a_int(cadena):
        try:
            return int(cadena) 
        except ValueError:
            try:
                return int(float(cadena)) 
            except ValueError:
                return int(0)

    url = "https://snia.mop.gob.cl/controlextraccion/datosExtraccion/SendDataExtraccionService"
    codigo_obra= profile_data.code_dga_site
    type_dga = profile_data.type_dga
    time_stamp_origen=response['date_time_medition']+'Z'
    fecha_medicion=str(response['date_time_medition'][8:10]+'-'+response['date_time_medition'][5:7]+'-'+response['date_time_medition'][0:4])
    hora_medicion=str(response['date_time_medition'][11:19])
    totalizador=convertir_a_int(response['total'])
    caudal=float(response['flow'])
    rut = profile_data.rut_report_dga
    password = profile_data.password_dga_software
    id_interaction = response['id_data']
    nivel_freatico_del_pozo = round(float(profile_data.d3) - float(response['nivel']),1) if response['nivel'] is not None else 0


    if(caudal<0):
        caudal = 0.0

    if(nivel_freatico_del_pozo<0):
        nivel_freatico_del_pozo = 0.0

    if(type_dga=='SUB'):
        payload = str("<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:aut=\"http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionRequest\">\n<soapenv:Header>\n<aut:authSendDataExtraccionTraza>\n<aut:codigoDeLaObra>{codigo_obra}</aut:codigoDeLaObra>\n<aut:timeStampOrigen>{time_stamp_origen}</aut:timeStampOrigen>\n</aut:authSendDataExtraccionTraza>\n</soapenv:Header>\n<soapenv:Body>\n<aut:authSendDataExtraccionRequest>\n<aut:authDataUsuario>\n<aut:idUsuario>\n<aut:rut>{rut}</aut:rut>\n</aut:idUsuario>\n<aut:password>{password}</aut:password>\n</aut:authDataUsuario>\n<!--Optional:-->\n<aut:authDataExtraccionSubterranea>\n<aut:fechaMedicion>{fecha_medicion}</aut:fechaMedicion>\n<aut:horaMedicion>{hora_medicion}</aut:horaMedicion>\n<aut:totalizador>{totalizador}</aut:totalizador>\n<aut:caudal>{caudal}</aut:caudal>\n<aut:nivelFreaticoDelPozo>{nivel_freatico_del_pozo}</aut:nivelFreaticoDelPozo>\n</aut:authDataExtraccionSubterranea>\n</aut:authSendDataExtraccionRequest>\n</soapenv:Body>\n</soapenv:Envelope>").format(totalizador=int(totalizador), rut=rut, password=password, caudal=caudal, nivel_freatico_del_pozo=nivel_freatico_del_pozo, codigo_obra=codigo_obra, time_stamp_origen=time_stamp_origen, fecha_medicion=fecha_medicion, hora_medicion=hora_medicion)
    else:
        payload = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:aut="http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionRequest">
        <soapenv:Header>
            <aut:authSendDataExtraccionTraza>
                <aut:codigoDeLaObra>{codigo_obra}</aut:codigoDeLaObra>
                <aut:timeStampOrigen>{time_stamp_origen}</aut:timeStampOrigen>
            </aut:authSendDataExtraccionTraza>
        </soapenv:Header>
        <soapenv:Body>
            <aut:authSendDataExtraccionRequest>
                <aut:authDataUsuario>
                    <aut:idUsuario>
                        <aut:rut>{rut}</aut:rut>
                    </aut:idUsuario>
                    <aut:password>{password}</aut:password>
                </aut:authDataUsuario>
                <aut:authDataExtraccionSuperficial> <!-- Corregir aquí -->
                    <aut:fechaMedicion>{fecha_medicion}</aut:fechaMedicion>
                    <aut:horaMedicion>{hora_medicion}</aut:horaMedicion>
                    <aut:totalizador>{totalizador}</aut:totalizador>
                    <aut:caudal>{caudal}</aut:caudal>
                    <aut:alturaLimnimetrica>{nivel_freatico_del_pozo}</aut:alturaLimnimetrica>
                </aut:authDataExtraccionSuperficial> <!-- Corregir aquí -->
            </aut:authSendDataExtraccionRequest>
        </soapenv:Body>
    </soapenv:Envelope>
    """.format(totalizador=int(totalizador), rut=rut, password=password, caudal=caudal, nivel_freatico_del_pozo=nivel_freatico_del_pozo, codigo_obra=codigo_obra, time_stamp_origen=time_stamp_origen, fecha_medicion=fecha_medicion, hora_medicion=hora_medicion)




    headers = {
      'Content-Type': 'application/xml'
    }


    response = requests.request("POST", url, headers=headers, data=payload)
    
    root = ET.fromstring(response.text)
    description = root.find('.//{http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionResponse}Description')
    code = root.find('.//{http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionResponse}Code')
    
    is_send = False

    if code.text == '0':
        is_send=True

    # Verifica si la respuesta fue exitosa (código de estado 200)
    if response.status_code == 200:
    # Intenta analizar la respuesta como XML
        try:
            root = ET.fromstring(response.text)
        # Ahora puedes continuar con el procesamiento del XML si es necesario
        except ET.ParseError as e:
            description = f"Error al analizar la respuesta XML: {e}"
    else:
        description = f"Error en la solicitud. Código de estado: {response.status_cod}"

    description_parser = ('{code}) {description}').format(code=code.text, description=description.text)
    InteractionDetail.objects.filter(id=id_interaction).update(soap_return=description_parser, is_send_dga=is_send)
