from zeep import Client
import requests
from datetime import datetime



def send(profile_data, response):
    url = "https://snia.mop.gob.cl/controlextraccion/datosExtraccion/SendDataExtraccionService"

    codigo_obra= profile_data.code_dga_site
    time_stamp_origen=response['date_time_medition']+'Z'
    fecha_medicion=str(response['date_time_medition'][8:10]+'-'+response['date_time_medition'][5:7]+'-'+response['date_time_medition'][0:4])
    hora_medicion=str(response['date_time_medition'][11:19])
    totalizador=int(response['total'])
    caudal=float(response['flow'])
    nivel_freatico_del_pozo=float(profile_data.d3)-float(response['nivel'])


    payload = ("<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:aut=\"http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionRequest\">\n<soapenv:Header>\n<aut:authSendDataExtraccionTraza>\n<aut:codigoDeLaObra>{codigo_obra}</aut:codigoDeLaObra>\n<aut:timeStampOrigen>{time_stamp_origen}</aut:timeStampOrigen>\n</aut:authSendDataExtraccionTraza>\n</soapenv:Header>\n<soapenv:Body>\n<aut:authSendDataExtraccionRequest>\n<aut:authDataUsuario>\n<aut:idUsuario>\n<aut:rut>17352192-8</aut:rut>\n</aut:idUsuario>\n<aut:password>ZSQgCiDg7y</aut:password>\n</aut:authDataUsuario>\n<!--Optional:-->\n<aut:authDataExtraccionSubterranea>\n<aut:fechaMedicion>{fecha_medicion}</aut:fechaMedicion>\n<aut:horaMedicion>{hora_medicion}</aut:horaMedicion>\n<aut:totalizador>{totalizador}</aut:totalizador>\n<aut:caudal>{caudal}</aut:caudal>\n<aut:nivelFreaticoDelPozo>{nivel_freatico_del_pozo}</aut:nivelFreaticoDelPozo>\n</aut:authDataExtraccionSubterranea>\n</aut:authSendDataExtraccionRequest>\n</soapenv:Body>\n</soapenv:Envelope>").format(totalizador=totalizador, 
            caudal=caudal, 
            nivel_freatico_del_pozo=nivel_freatico_del_pozo, 
            codigo_obra=codigo_obra, 
            time_stamp_origen=time_stamp_origen, 
            fecha_medicion=fecha_medicion, 
            hora_medicion=hora_medicion)

    headers = {
      'Content-Type': 'application/xml'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print(profile_data)
    print(response.text)



