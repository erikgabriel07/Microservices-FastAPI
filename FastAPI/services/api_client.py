import requests
from fastapi.responses import JSONResponse
from fastapi import status as s
from config.urls import Flask_URL as url


def get_token(user, pwd, file_processor):
    try:
        response = requests.post(url.FLASK_LOGIN_ROUTE, json={'user': user, 'pwd': pwd})
        response.raise_for_status()
    except Exception as e:
        JSONResponse(status_code=s.HTTP_400_BAD_REQUEST,
                     content={'mensagem': 'Ocorreu um erro durante a requisição!',
                              'error': str(e)})
    if response.status_code == 200:
        file_processor.set_token(response.json()['access_token'])
    return response.json()

def send_data(data, header):
    try:
        response = requests.post(url.FLASK_BASE_INCIDENCIA_URL, json=data, headers=header)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao enviar dados: {e}")