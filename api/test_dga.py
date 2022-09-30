import zeep
import requests


wsdl = 'http://snia.mop.gob.cl/controlextraccion/wsdl/datosExtraccion/SendDataExtraccionService'

#header_url = 'http://www.mop.cl/controlextraccion/xsd/datosExtraccion/SendDataExtraccionRequest'

client = zeep.Client(wsdl=wsdl)

payload = """
    <x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:aut1="http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionRequest">
        <x:Header>
            <aut1:authSendDataExtraccionTraza>
                <aut1:codigoDeLaObra>OB-0901-78</aut1:codigoDeLaObra>
                <aut1:timeStampOrigen>2021-08-06T14:01:00Z</aut1:timeStampOrigen>
            </aut1:authSendDataExtraccionTraza>
        </x:Header>
        <x:Body>
            <aut1:authSendDataExtraccionRequest>
                <aut1:authDataUsuario>
                    <aut1:idUsuario>
                        <aut1:rut>55555555-5</aut1:rut>
                    </aut1:idUsuario>
                    <aut1:password>QD4W5AfMNB</aut1:password>
                </aut1:authDataUsuario>
                <aut1:authDataExtraccionSubterranea>
                    <aut1:fechaMedicion>06-08-2021</aut1:fechaMedicion>
                    <aut1:horaMedicion>14:59:00</aut1:horaMedicion>
                    <aut1:totalizador>7878</aut1:totalizador>
                    <aut1:caudal>2.34</aut1:caudal>
                    <aut1:nivelFreaticoDelPozo>37.21</aut1:nivelFreaticoDelPozo>
                </aut1:authDataExtraccionSubterranea>
            </aut1:authSendDataExtraccionRequest>
        </x:Body>
    </x:Envelope>
"""

response = requests.request("POST", wsdl, data=payload)
print(response.text)
print(response)

header_value = {
    "authSendDataExtraccionTraza" : {
        "codigoDeLaObra" : "OB-0803-39",
        "timeStampOrigen" : "2022-09-27T11:00:00Z"
    }
}

client.set_default_soapheaders(header_value)
"""execute_service = client.service.authSendDataExtraccionOp(
        authDataUsuario={
            'idUsuario':'17352192-8', 
            'password':'ZSQgCiDg7y'
        },
        authDataExtraccionSubterranea={
            'fechaMedicion': '06-08-2021',
            'horaMedicion': '14:59:00',
            'totalizador': '7878',
            'caudal': '2.34',
            'nivelFreaticoDelPozo':'37.21'
        })"""


