import zeep
from zeep import xsd
import json 


wsdl = 'https://snia.mop.gob.cl/controlextraccion/wsdl/datosExtraccion/SendDataExtraccionService?wsdl'
client = zeep.Client(wsdl=wsdl)

print(dir(client.plugins))


"""execute_service = client.service.authSendDataExtraccionOp(
        authDataUsuario={
            'idUsuario':'17829231-5', 
            'password':'asdasd'
        },
        authDataExtraccionSubterranea={
            'fechaMedicion': '06-08-2021',
            'horaMedicion': '14:59:00',
            'totalizador': '7878',
            'caudal': '2.34',
            'nivelFreaticoDelPozo':'37.21'
        })"""



