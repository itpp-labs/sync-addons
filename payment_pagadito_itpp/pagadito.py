# -*- coding: utf-8 -*-
# Copyright 2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import json
import logging

_logger = logging.getLogger(__name__)


try:
    from zeep import Client
except ImportError as err:
    Client = None
    _logger.debug(err)

# from WSPG section of Pagadito docs
# https://dev.pagadito.com/index.php?mod=docs&hac=wspg

PG_CONNECT_SUCCESS = "PG1001"  # Connection successful.	X	X	Conexión exitosa del Pagadito Comercio con el WSPG.
PG_EXEC_TRANS_SUCCESS = "PG1002"  # Transaction register successful.	X	X	La transacción enviada por el Pagadito Comercio fue registrada correctamente por el WSPG.
PG_GET_STATUS_SUCCESS = "PG1003"  # Transaction status.	X	X	Ha sido procesada correctamente la petición de estado de transacción.
# PG_ = "PG1004"  #	Exchange Rate.	X	X	Ha sido procesada correctamente la petición de tasa de cambio.
# PG_ = "PG2001"  #	Incomplete data.		X	El Pagadito Comercio no envió todos los parámetros necesarios.
# PG_ = "PG2002"  #	Incorrect format data.		X	El formato de los datos enviados por el Pagadito Comercio no es el correcto.
# PG_ = "PG3001"  #	Connection couldn't be established.		X	Las credenciales de conexión no están registradas.
# PG_ = "PG3002"  #	We're sorry. An error has occurred.		X	Un error no controlado por el WSPG ocurrió y no se ha podido procesar la petición.
# PG_ = "PG3003"  #	Unregistered transaction.		X	La transacción solicitada no ha sido registrada.
# PG_ = "PG3004"  #	Transaction amount doesn't match with calculated amount.		X	La suma de los productos de la cantidad y el precio de los detalles no es igual al monto de la trasacción.
# PG_ = "PG3005"  #	Connection is disabled.		X	El Pagadito Comercio ha sido validado, pero la conexión se encuentra deshabilitada.
# PG_ = "PG3006"  #	Amount has exceeded the maximum.		X	La transacción ha sido denegada debido a que excede el monto máximo por transacción.
# PG_ = "PG3007"  #	Denied access.		X	El acceso ha sido denegado, debido a que el token no es válido.
# PG_ = "PG3008"  #	Currency not supported.		X	La moneda solicitada no es soportada por Pagadito.
# PG_ = "PG3009"  #	Amount is lower than the minimum allowed.		X	La transacción ha sido denegada debido a que el monto es menor al mínimo permitido.

STATUS_REGISTERED = "REGISTERED"  # La transacción ha sido registrada correctamente en Pagadito, pero aún se encuentra en proceso. En este punto, el cobro aún no ha sido realizado.
STATUS_COMPLETED = "COMPLETED"  # X	X	La transacción ha sido procesada correctamente en Pagadito. En este punto el cobro ya ha sido realizado.
STATUS_VERIFYING = "VERIFYING"  # X	X	La transacción ha sido procesada en Pagadito, pero ha quedado en verificación. En este punto el cobro ha quedado en validación administrativa. Posteriormente, la transacción puede marcarse como válida o denegada; por lo que se debe monitorear mediante esta función hasta que su estado cambie a COMPLETED o REVOKED.
STATUS_REVOKED = "REVOKED"  # X	X	La transacción en estado VERIFYING ha sido denegada por Pagadito. En este punto el cobro ya ha sido cancelado.
STATUS_FAILED = "FAILED"  # La transacción ha sido registrada correctamente en Pagadito, pero no pudo ser procesada. En este punto, el cobro aún no ha sido realizado.
STATUS_CANCELED = "CANCELED"  # La transacción ha sido cancelada por el usuario en Pagadito, la transacción tiene este estado cuando el usuario hace click en el enlace de "regresar al comercio" en la pantalla de pago de Pagadito.
STATUS_EXPIRED = "EXPIRED"  # La transacción ha expirado en Pagadito, la transacción tiene este estado cuando se termina el tiempo para completar la transacción por parte del usuario en Pagadito, el tiempo para completar la transacción en Pagadito por parte del usuario es de 10 minutos. Pagadito también se encarga de poner estado EXPIRED a todas las transacciones que no fueron completas, debido a que el usuario salio de manera inesperada del proceso de pago, por ejemplo cerrando la ventana del navegador.

SUPPORTED_CURRENCY = [
    "USD",  # Valor por defecto. Dólares americanos.
    "GTQ",  # Quetzales.
    "HNL",  # Lempiras.
    "NIO",  # Córdobas.
    "CRC",  # Colones costarricenses.
    "PAB",  # Balboas.
    "DOP",  # Pesos dominicanos.
]

# operation list
OP_CONNECT = "connect"
OP_EXEC_TRANS = "exec_trans"
OP_GET_STATUS = "get_status"

SANDBOX2WSDL_URL = {
    True: "https://sandbox.pagadito.com/comercios/wspg/charges.php?wsdl",
    False: "https://comercios.pagadito.com/wspg/charges.php?wsdl",
}
sandbox2client = {}


def get_client(sandbox=True):
    """Returns cached client or creates new one"""
    global client
    client = sandbox2client.get(sandbox)
    if not client:
        url = SANDBOX2WSDL_URL[sandbox]
        client = Client(url)
        sandbox2client[sandbox] = client

    return client


def call(operation, params=None, sandbox=True):
    params["format_return"] = "json"
    _logger.debug('Call "%s" in sandbox=%s with args:\n%s', operation, sandbox, params)
    client = get_client(sandbox)
    operation = getattr(client.service, operation)
    params = params or {}
    response = operation(**params)

    _logger.debug("Raw response:\n%s", response)
    res_json = json.loads(response)
    return res_json
