import requests
from datetime import datetime
from core.compra import Compra

fecha_actual = datetime.now()
fecha_actual = fecha_actual.strftime("%Y-%m-%d")

def cambio_moneda(codigo):
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=meyesblue@gmail.com&pass=ASDFghjk1&firstdate='+fecha_actual+'&timeseries='+codigo+'&function=GetSeries'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        valor = data['Series']['Obs'][0]['value']
        print("💚 ", valor)
        return valor
    else:
        print('Error al consultar la API del Banco Central de Chile')


def agregar(request, id_producto):
    url = 'http://127.0.0.1:8001/'
    url_productos = url + 'lista_productos/'
    url_stocks = url + 'lista_stocks/'
    url_precios = url + 'lista_precios/'

    try:
            response_productos = requests.get(url_productos)
            response_stocks = requests.get(url_stocks)
            response_precios = requests.get(url_precios)

            if response_productos.status_code == 200:
                data_productos = response_productos.json()
                data_precios = response_precios.json()

                productos = [type('', (object,), item)() for item in data_productos]
                precios = [type('', (object,), item)() for item in data_precios]

                
            producto = None
            precio = None
            compra = Compra(request)
            numero = int(id_producto)
            for p in productos:
                if p.id_producto == numero:
                    producto = p.nombre
                    for n in precios:
                        if n.id_producto == numero:
                                if fecha_actual >= n.fec_ini and fecha_actual <= n.fec_ter:
                                    precio = n.precio

            
            compra.agregar(id_producto, producto, precio)

    except Exception as e:
            print('Ocurrió un error:', e)


def restar(request, id_producto):
    url = 'http://127.0.0.1:8001/'
    url_productos = url + 'lista_productos/'
    url_precios = url + 'lista_precios/'

    try:
            response_productos = requests.get(url_productos)
            response_precios = requests.get(url_precios)

            if response_precios.status_code == 200:
                data_productos = response_productos.json()
                data_precios = response_precios.json()

                productos = [type('', (object,), item)() for item in data_productos]
                precios = [type('', (object,), item)() for item in data_precios]

                print("VAMOOOOOOOO")
                precio = None
                compra = Compra(request)
                numero = int(id_producto)
                for p in productos:
                    if p.id_producto == numero:
                        for n in precios:
                            if n.id_producto == numero:
                                if fecha_actual >= n.fec_ini and fecha_actual <= n.fec_ter:
                                    precio = n.precio
                

                compra.restar(numero, precio)


    except Exception as e:
            print('Ocurrió un error:', e)