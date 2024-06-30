import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from .utils import cambio_moneda
from .views import agregar_producto, restar_producto, initiate_payment, dolar, euro
from rest_framework import status

import requests
from datetime import datetime

class TransbankTests(TestCase):

    #TEST PAGO EXITOSO
    @patch('transbank.webpay.webpay_plus.transaction.Transaction.commit')
    def test_confirm_payment_success(self, mock_commit):
        mock_commit.return_value = {'status': 'AUTHORIZED'}
        client = Client()
        response = client.get(reverse('confirm_payment'), {'token_ws': 'fake-token'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/success.html')

    #TEST PAGO RECHAZADO
    @patch('transbank.webpay.webpay_plus.transaction.Transaction.commit')
    def test_payment_failure(self, mock_commit):
        mock_commit.return_value = {'status': 'REJECTED'}
        client = Client()
        response = client.get(reverse('confirm_payment'), {'token_ws': 'fake-token'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/failure.html')

class CambioMonedaTests(TestCase):

    #TEST CAMBIO MONEDA EXITOSO
    @patch('requests.get')
    def test_cambio_moneda_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'Series': {
                'Obs': [{'value': '944'}] 
            }
        }
        mock_get.return_value = mock_response

        url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx'

        response = requests.get(url, params={
            'user': 'meyesblue@gmail.com',
            'pass': 'ASDFghjk1',
            'firstdate': '2024-06-30',
            'timeseries': 'F073.TCO.PRE.Z.D',
            'function': 'GetSeries'
        })

        self.assertEqual(response.status_code, 200)

        data = response.json()
        print("DATA QUE LLEGA ", data)
        valor = data['Series']['Obs'][0]['value']
        print("VALOR QUE SE RECUPERA ", valor)

        valor = int(valor)

        print("VALOR DOLAR QUE LE PASO ",dolar)

        self.assertEqual(valor, dolar)



    #TEST CAMBIO DE MONEDA FALLIDO
    @patch('requests.get')
    def test_cambio_moneda_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        valor = cambio_moneda("codigo_erroneo")
        self.assertIsNone(valor)

class APITests(TestCase):

    #TEST API PRODUCTO INEXISTENTE
    def test_ingreso_producto_inexistente(self):
        datos_producto = {
            "nombre": "Producto Inexistente",
            "id_tipo": "Herramientas Manuales"
        }

        url_lista_productos = 'http://127.0.0.1:8001/lista_productos/'

        response = self.client.post(url_lista_productos, datos_producto, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



