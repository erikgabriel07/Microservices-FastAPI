import requests
from fastapi.responses import JSONResponse
from fastapi import status as s
from config.urls import Flask_URL as url
from fastapi.exceptions import HTTPException


def list_file(header, bi=False, tc=False):
    try:
        if bi == tc:
            raise HTTPException(
                status_code=s.HTTP_400_BAD_REQUEST,
                detail={'mensagem': 'Apenas um e somente um parâmetro pode ser selecionado.'}
            )

        response = requests.get(
            url.FLASK_LIST_DATA_URL,
            headers=header,
            json={'bi': bi, 'tc': tc}
        )
        response.raise_for_status()

    except Exception as e:
        raise HTTPException(
            status_code=s.HTTP_400_BAD_REQUEST,
            detail={'mensagem': 'Erro durante o processamento da requisição.', 'error': str(e)}
        )
    return response.json()


def get_token(user, pwd, file_processor):
    try:
        if file_processor.get_token():
            response = requests.post(
                url.FLASK_LOGIN_ROUTE,
                json={'user': user, 'pwd': pwd, 'token': file_processor.get_token()}
            )
        else:
            response = requests.post(
                url.FLASK_LOGIN_ROUTE,
                json={'user': user, 'pwd': pwd}
            )
        response.raise_for_status()

    except Exception as e:
        return JSONResponse(
            status_code=s.HTTP_400_BAD_REQUEST,
            content={'mensagem': 'Ocorreu um erro durante a requisição!', 'error': str(e)}
        )

    if response.status_code == 200:
        file_processor.set_token(response.json()['access_token'])
    return response.json()


def send_data(data, header, file):
    try:
        # Define a URL com base no tipo de arquivo
        if file.filename == "Tabela 1 - Base de Incidência.csv":
            url_to_use = url.FLASK_BASE_INCIDENCIA_URL
        elif file.filename == "Tabela 2 - Tributo e Competência.csv":
            url_to_use = url.FLASK_TRIBUTO_COMPETENCIA_URL
        else:
            raise ValueError(
                "Arquivo inválido. O arquivo deve ser 'Tabela 1 - Base de Incidência' "
                "ou 'Tabela 2 - Tributo e Competência'"
            )

        # Faz a requisição usando a URL apropriada
        response = requests.post(url_to_use, json=data, headers=header)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao enviar dados: {e}")

    except ValueError as ve:
        raise Exception(ve)
